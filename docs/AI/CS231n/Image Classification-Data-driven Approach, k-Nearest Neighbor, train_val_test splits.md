# Image Classification-Data-driven Approach, k-Nearest Neighbor, train_val_test splits

## image classification

- challenges
	- viewpoint variation
	- scale variation
	- deformation
	- occlusion
	- illumination conditions
	- background clutter
	- intra-class variation
- data-driven approach
- the image classification pipeline
	- input
	- learning
		- training a classifier
		- learning a model
	- evaluation

## Nearest Neighbor Classifier

$$
d_1 (I_1, I_2) = \sum_{p} \left| I^p_1 - I^p_2 \right|
$$

```python
import numpy as np

class NearestNeighbor(object):  
  def **init**(self):  
    pass

  def train(self, X, y):  
    """ X is N x D where each row is an example. Y is 1-dimension of size N """  
    # the nearest neighbor classifier simply remembers all the training data  
    self.Xtr = X  
    self.ytr = y

  def predict(self, X):  
    """ X is N x D where each row is an example we wish to predict label for """  
    num_test = X.shape[0]  
    # lets make sure that the output type matches the input type  
    Ypred = np.zeros(num_test, dtype = self.ytr.dtype)

    # loop over all test rows
    for i in range(num_test):
      # find the nearest training image to the i'th test image
      # using the L1 distance (sum of absolute value differences)
      distances = np.sum(np.abs(self.Xtr - X[i,:]), axis = 1)
      min_index = np.argmin(distances) # get the index with smallest distance
      Ypred[i] = self.ytr[min_index] # predict the label of the nearest example

    return Ypred
```

$$
d_2 (I_1, I_2) = \sqrt{\sum_{p} \left( I^p_1 - I^p_2 \right)^2}
$$

```python
distances = np.sqrt(np.sum(np.square(self.Xtr - X[i,:]), axis = 1))
```

## k - Nearest Neighbor Classifier

![[Pasted image 20241031202452.jpg]]

## Validation sets for Hyperparameter tuning

> Evaluate on the test only a single time, at the very end

>Split your training set into training set and a validation set. Use validation set to tune all hyperparameters. At the end run a single time on the test set and report performance.

- cross-validation
- single calidation split  
![[Pasted image 20241031202849.png]]

## Pros and Cons of Nearest Neighbor classifier

- simple to implement and understand
- take no time to train
- however, pay a cost at test time

>As an aside, the computational complexity of the Nearest Neighbor classifier is an active area of research, and several **Approximate Nearest Neighbor** (ANN) algorithms and libraries exist that can accelerate the nearest neighbor lookup in a dataset (e.g. [FLANN](https://github.com/mariusmuja/flann)). These algorithms allow one to trade off the correctness of the nearest neighbor retrieval with its space/time complexity during retrieval, and usually rely on a pre-processing/indexing stage that involves building a kdtree, or running the k-means algorithm.

- $\displaystyle L_{2}$ isn't enough sensitive

>In particular, note that images that are nearby each other are much more a function of the general color distribution of the images, or the type of background rather than their semantic identity.

> [!note]+ Applying kNN in practice
> 1. Preprocess your data: Normalize the features in your data (e.g. one pixel in images) to have zero mean and unit variance. We will cover this in more detail in later sections, and chose not to cover data normalization in this section because pixels in images are usually homogeneous and do not exhibit widely different distributions, alleviating the need for data normalization.
> 2. If your data is very high-dimensional, consider using a dimensionality reduction technique such as PCA ([wiki ref](https://en.wikipedia.org/wiki/Principal_component_analysis), [CS229ref](http://cs229.stanford.edu/notes/cs229-notes10.pdf), [blog ref](https://web.archive.org/web/20150503165118/http://www.bigdataexaminer.com:80/understanding-dimensionality-reduction-principal-component-analysis-and-singular-value-decomposition/)), NCA ([wiki ref](https://en.wikipedia.org/wiki/Neighbourhood_components_analysis), [blog ref](https://kevinzakka.github.io/2020/02/10/nca/)), or even [Random Projections](https://scikit-learn.org/stable/modules/random_projection.html).
> 3. Split your training data randomly into train/val splits. As a rule of thumb, between 70-90% of your data usually goes to the train split. This setting depends on how many hyperparameters you have and how much of an influence you expect them to have. If there are many hyperparameters to estimate, you should err on the side of having larger validation set to estimate them effectively. If you are concerned about the size of your validation data, it is best to split the training data into folds and perform cross-validation. If you can afford the computational budget it is always safer to go with cross-validation (the more folds the better, but more expensive).
> 4. Train and evaluate the kNN classifier on the validation data (for all folds, if doing cross-validation) for many choices of **k** (e.g. the more the better) and across different distance types (L1 and L2 are good candidates)
> 5. If your kNN classifier is running too long, consider using an Approximate Nearest Neighbor library (e.g. [FLANN](https://github.com/mariusmuja/flann)) to accelerate the retrieval (at cost of some accuracy).
> 6. Take note of the hyperparameters that gave the best results. There is a question of whether you should use the full training set with the best hyperparameters, since the optimal hyperparameters might change if you were to fold the validation data into your training set (since the size of the data would be larger). In practice it is cleaner to not use the validation data in the final classifier and consider it to be _burned_ on estimating the hyperparameters. Evaluate the best model on the test set. Report the test set accuracy and declare the result to be the performance of the kNN classifier on your data.

[[more about Machine Learing]]
