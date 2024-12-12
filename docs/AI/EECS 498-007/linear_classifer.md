## 原理

两种线性分类器：支持向量机（SVM）和Softmax分类器。这两种分类器都是监督学习算法，用于分类任务。

### 支持向量机（SVM）

SVM的目标是找到一个超平面，它可以最大化不同类别之间的边界。这个超平面被称为最优分割超平面。对于二分类问题，SVM的损失函数可以表示为：

$$
L(W, b) = \frac{1}{N} \sum_{i=1}^{N} \max(0, 1 - y_i (W \cdot x_i + b))
$$

其中，$W$ 是权重向量，$b$ 是偏置项，$x_i$ 是输入特征，$y_i$ 是标签（-1或1），$N$ 是样本数量。

为了实现多分类，我们使用结构化SVM损失函数，它考虑了每个类别的分数，并尝试最大化正确类别的分数与次高类别分数之间的差距。损失函数可以表示为：

$$
L(W) = \frac{1}{N} \sum_{i=1}^{N} \sum_{j \neq y_i} \max(0, \text{score}_j - \text{score}_{y_i} + \Delta)
$$

其中，$\text{score}_j = W_j \cdot x_i$，$\Delta$ 是一个常数，通常设置为1。

### Softmax分类器

Softmax分类器使用Softmax函数将输入特征映射到概率分布上。对于每个样本，Softmax函数输出每个类别的概率。Softmax函数定义为：

$$
\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}
$$

其中，$z_i$ 是第$i$个类别的分数，$K$ 是类别总数。

Softmax分类器的损失函数是交叉熵损失，可以表示为：

$$
L(W) = -\frac{1}{N} \sum_{i=1}^{N} \sum_{j=1}^{K} y_{ij} \log(\text{softmax}(z_j))
$$

其中，$y_{ij}$ 是一个指示变量，如果样本$i$属于类别$j$，则为1，否则为0。

### 正则化

为了防止过拟合，我们在损失函数中添加了正则化项。L2正则化的损失函数可以表示为：

$$
L(W) = L(W) + \lambda \lVert W \rVert^2
$$

其中，$\lambda$ 是正则化强度。

### 代码实现

代码中实现了两种损失函数的朴素版本（`svm_loss_naive` 和 `softmax_loss_naive`）和向量化版本（`svm_loss_vectorized` 和 `softmax_loss_vectorized`）。向量化版本通过避免显式循环来提高计算效率。

训练过程（`train_linear_classifier`）使用随机梯度下降（SGD）来优化损失函数。在每次迭代中，我们随机抽取一个批次的样本，计算损失和梯度，然后更新权重。

预测过程（`predict_linear_classifier`）使用训练好的权重来预测新样本的类别。

### 超参数搜索

代码中还包含了超参数搜索的函数（`svm_get_search_params` 和 `softmax_get_search_params`），它们返回不同的学习率和正则化强度的候选值，以便找到最佳的模型参数。

## 作业实现

```python
import torch
import random
from abc import abstractmethod

def hello_linear_classifier():
  print('Hello from linear_classifier.py!')

class LinearClassifier(object):
  def __init__(self):
    random.seed(0)
    torch.manual_seed(0)
    self.W = None

  def train(self, X_train, y_train, learning_rate=1e-3, reg=1e-5, num_iters=100,
            batch_size=200, verbose=False):
    train_args = (self.loss, self.W, X_train, y_train, learning_rate, reg,
                  num_iters, batch_size, verbose)
    self.W, loss_history = train_linear_classifier(*train_args)
    return loss_history

  def predict(self, X):
    return predict_linear_classifier(self.W, X)

  @abstractmethod
  def loss(self, W, X_batch, y_batch, reg):
    raise NotImplementedError

  def _loss(self, X_batch, y_batch, reg):
    self.loss(self.W, X_batch, y_batch, reg)

  def save(self, path):
    torch.save({'W': self.W}, path)
    print("Saved in {}".format(path))

  def load(self, path):
    W_dict = torch.load(path, map_location='cpu')
    self.W = W_dict['W']
    print("load checkpoint file: {}".format(path))


class LinearSVM(LinearClassifier):
  def loss(self, W, X_batch, y_batch, reg):
    return svm_loss_vectorized(W, X_batch, y_batch, reg)


class Softmax(LinearClassifier):
  def loss(self, W, X_batch, y_batch, reg):
    return softmax_loss_vectorized(W, X_batch, y_batch, reg)


def svm_loss_naive(W, X, y, reg):
  dW = torch.zeros_like(W)
  num_classes = W.shape[1]
  num_train = X.shape[0]
  loss = 0.0
  for i in range(num_train):
    scores = W.t().mv(X[i])
    correct_class_score = scores[y[i]]
    for j in range(num_classes):
      if j == y[i]:
        continue
      margin = scores[j] - correct_class_score + 1
      if margin > 0:
        loss += margin
        dW[:, j] += X[i]
        dW[:, y[i]] -= X[i]

  loss /= num_train
  loss += reg * torch.sum(W * W)
  dW /= num_train
  dW += 2 * reg * W

  return loss, dW


def svm_loss_vectorized(W, X, y, reg):
  loss = 0.0
  dW = torch.zeros_like(W)
  num_classes = W.shape[1]
  num_train = X.shape[0]
  scores = X.mm(W)
  correct_class_score = scores[range(num_train), y]
  margin = scores - correct_class_score.view(-1, 1) + 1
  margin[range(num_train), y] = 0
  mask = (margin > 0)
  loss = margin[mask].sum()
  mask_correct_y = torch.zeros_like(scores, dtype=torch.bool)
  mask_correct_y[range(num_train), y] = True
  margin[margin > 0] = 1
  margin[margin < 0] = 0
  margin[mask_correct_y] = torch.sum(margin, axis=1) * -1
  dW = margin.T.mm(X).T
  loss /= num_train
  dW /= num_train
  loss += reg * torch.sum(W * W)
  dW += 2 * reg * W

  return loss, dW


def sample_batch(X, y, num_train, batch_size):
  indices = torch.randint(num_train, (batch_size,))
  y_batch = y[indices]
  X_batch = X[indices]
  return X_batch, y_batch


def train_linear_classifier(loss_func, W, X, y, learning_rate=1e-3,
                            reg=1e-5, num_iters=100, batch_size=200,
                            verbose=False):
  num_train, dim = X.shape
  if W is None:
    num_classes = torch.max(y) + 1
    W = 0.000001 * torch.randn(dim, num_classes, device=X.device, dtype=X.dtype)
  else:
    num_classes = W.shape[1]

  loss_history = []
  for it in range(num_iters):
    X_batch, y_batch = sample_batch(X, y, num_train, batch_size)
    loss, grad = loss_func(W, X_batch, y_batch, reg)
    loss_history.append(loss.item())
    W -= learning_rate * grad
    if verbose and it % 100 == 0:
      print('iteration %d / %d: loss %f' % (it, num_iters, loss))

  return W, loss_history


def predict_linear_classifier(W, X):
  y_pred = torch.zeros(X.shape[0], dtype=torch.int64)
  _, y_pred = X.mm(W).max(dim=1)
  return y_pred


def svm_get_search_params():
  learning_rates = [0.000001, 0.0001, 0.001, 0.005, 0.01, 0.05]
  regularization_strengths = [0.001, 0.5, 1, 3]
  return learning_rates, regularization_strengths


def test_one_param_set(cls, data_dict, lr, reg, num_iters=2000):
  train_acc = 0.0
  val_acc = 0.0
  cls.train(data_dict['X_train'], data_dict['y_train'], lr, reg, num_iters,
            batch_size=200, verbose=False)
  y_train_pred = cls.predict(data_dict['X_train'])
  train_acc = 100.0 * (data_dict['y_train'] == y_train_pred).double().mean().item()

  y_test_pred = cls.predict(data_dict['X_val'])
  val_acc = 100.0 * (data_dict['y_val'] == y_test_pred).double().mean().item()

  return cls, train_acc, val_acc


def softmax_loss_naive(W, X, y, reg):
  loss = 0.0
  dW = torch.zeros_like(W)
  num_classes = W.shape[1]
  num_train = X.shape[0]
    
  scores = W.t().mv(X[0])
  correct_class_score = scores[y[0]]

  for i in range(num_train):
    scores = W.t().mv(X[i])
    scores = scores - scores.max()
    correct_class_score = scores[y[i]]
    loss += -correct_class_score + torch.log(torch.exp(scores).sum())
    for j in range(num_classes):
      if j == y[i]:
        dW[:, j] += torch.exp(scores[j]) / torch.exp(scores).sum() * X[i, :] - X[i, :]
      else:
        dW[:, j] += torch.exp(scores[j]) / torch.exp(scores).sum() * X[i, :]

  loss /= num_train
  loss += reg * torch.sum(W * W)
  dW /= num_train
  dW += 2 * reg * W

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  loss = 0.0
  dW = torch.zeros_like(W)
  num_classes = W.shape[1]
  num_train = X.shape[0]
    

  scores = X.mm(W)
  val, _ = scores.max(dim=1)
  scores = scores - val.view(-1, 1)
  exp_scores = scores.exp()
  exp_scores_sum = exp_scores.sum(dim=1)
  exp_scores_sum_log = exp_scores_sum.log()
  correct_class_scores = scores[range(num_train), y]
  loss = (exp_scores_sum_log - correct_class_scores).sum()
  zeros = torch.zeros((num_train, num_classes), dtype=torch.float64, device='cuda')
  zeros[range(num_train), y] = -1
  minus_X = zeros.t().mm(X)
  dW += minus_X.t()
  dW += ((exp_scores / exp_scores_sum.view(-1, 1)).t().mm(X)).t()

  loss /= num_train
  loss += reg * torch.sum(W * W)
  dW /= num_train
  dW += 2 * reg * W

  return loss, dW


def softmax_get_search_params():
  learning_rates = [1e-4, 1e-3,1e-2, 1e-1, 1]
  regularization_strengths = [1e-4, 1e-3, 1e-2, 1e-1] 
  return learning_rates, regularization_strengths
```
