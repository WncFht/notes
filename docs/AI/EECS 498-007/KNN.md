对于一个待分类的样本，找到训练数据集中与其最接近的K个样本（即最近邻），然后根据这K个样本的类别来决定待分类样本的类别。

## 数学推导

假设我们有一个训练数据集 $T = \{(x_1, y_1), (x_2, y_2), \ldots, (x_N, y_N)\}$，其中 $x_i$ 是特征向量， $y_i$ 是对应的类别标签。对于一个新的待分类样本 x，KNN算法的目标是预测其类别 $y$ 。

1. **距离度量**：首先，我们需要一个距离度量来计算待分类样本 $x$ 与训练集中每个样本 $x_i$ 之间的距离。常用的距离度量包括欧氏距离（Euclidean distance）、曼哈顿距离（Manhattan distance）和闵可夫斯基距离（Minkowski distance）。以欧氏距离为例，两个样本 $x$ 和 $x_i$ 之间的距离定义为：

$$
   d(x, x_i) = \sqrt{\sum_{j=1}^{d} (x_j - x_{i,j})^2}
$$

   其中， $d$ 是特征的维度。

2. **寻找最近邻**：然后，我们根据计算出的距离，选择距离最近的K个样本，构成待分类样本的邻域 $N_k(x)$。
3. **决策规则**：最后，根据邻域 \( N_k(x) \) 中的样本类别，通过多数投票的方式来决定待分类样本的类别。即：

$$
    y = \arg\max_{c_j} \sum_{x_i \in N_k(x)} I(y_i = c_j)
$$

   其中， $I$ 是指示函数，当 $y_i = c_j$ 时取值为1，否则为0。

## 作业中的实现

```python
import torch

def compute_distances_two_loops(x_train, x_test):
  num_train = x_train.shape[0]
  num_test = x_test.shape[0]
  dists = x_train.new_zeros(num_train, num_test)
  
  for i in range(num_train):
    for j in range(num_test):
      dists[i,j] = ((x_train[i] - x_test[j]) ** 2).sum() ** (1/2)
      
  return dists

def compute_distances_one_loop(x_train, x_test):
  num_train = x_train.shape[0]
  num_test = x_test.shape[0]
  dists = x_train.new_zeros(num_train, num_test)
  
  for i in range(num_train):
    dists[i] = ((x_train[i] - x_test) ** 2).sum(dim=(1,2,3)) ** (1/2)
    
  return dists

def compute_distances_no_loops(x_train, x_test):
  num_train = x_train.shape[0]
  num_test = x_test.shape[0]
  dists = x_train.new_zeros(num_train, num_test)
  
  A = x_train.reshape(num_train, -1)
  B = x_test.reshape(num_test, -1)
  AB2 = A.mm(B.T) * 2
  dists = ((A ** 2).sum(dim=1).reshape(-1, 1) - AB2 + (B ** 2).sum(dim=1).reshape(1, -1)) ** (1/2)
  
  return dists

def predict_labels(dists, y_train, k=1):
  num_train, num_test = dists.shape
  y_pred = torch.zeros(num_test, dtype=torch.int64)
  
  values, indices = torch.topk(dists, k, dim=0, largest=False)
  for i in range(indices.shape[1]):
    _, idx = torch.max(y_train[indices[:, i]].bincount(), dim=0)
    y_pred[i] = idx
    
  return y_pred

class KnnClassifier:
  def __init__(self, x_train, y_train):
    self.x_train = x_train
    self.y_train = y_train

  def predict(self, x_test, k=1):
    dists = compute_distances_no_loops(self.x_train, x_test)
    y_test_pred = predict_labels(dists, self.y_train, k)
    return y_test_pred

  def check_accuracy(self, x_test, y_test, k=1, quiet=False):
    y_test_pred = self.predict(x_test, k=k)
    num_samples = x_test.shape[0]
    num_correct = (y_test == y_test_pred).sum().item()
    accuracy = 100.0 * num_correct / num_samples
    msg = (f'Got {num_correct} / {num_samples} correct; accuracy is {accuracy:.2f}%')
    if not quiet:
      print(msg)
    return accuracy

def knn_cross_validate(x_train, y_train, num_folds=5, k_choices=None):
  if k_choices is None:
    k_choices = [1, 3, 5, 8, 10, 12, 15, 20, 50, 100]

  x_train_folds = torch.chunk(x_train, num_folds, dim=0)
  y_train_folds = torch.chunk(y_train, num_folds, dim=0)

  k_to_accuracies = {}

  for k in k_choices:
    list_of_acc = []
    for num_fold in range(num_folds):
      x_train_folds_local = [x for x in x_train_folds]
      y_train_folds_local = [x for x in y_train_folds]
      x_test = x_train_folds_local[num_fold]
      y_test = y_train_folds_local[num_fold]
      del x_train_folds_local[num_fold]
      del y_train_folds_local[num_fold]
      x_train = torch.cat(x_train_folds_local, dim=0)
      y_train = torch.cat(y_train_folds_local, dim=0)
      classifier = KnnClassifier(x_train, y_train)
      list_of_acc.append(classifier.check_accuracy(x_test, y_test, k))
    k_to_accuracies[k] = list_of_acc

  return k_to_accuracies

def knn_get_best_k(k_to_accuracies):
  best_k = 0
  new_dict = {}
  for k, accs in sorted(k_to_accuracies.items()):
    new_dict[k] = sum(accs) / len(accs) 
  max_value = max(new_dict.values())
  best_k = [k for k, v in new_dict.items() if v == max_value][0]
  return best_k
```
