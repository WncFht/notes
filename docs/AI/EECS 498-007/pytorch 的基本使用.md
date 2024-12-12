# pytorch 的基本使用

```python
# Create a rank 1 tensor from a Python list
a = torch.tensor([[1, 2, 3], [4, 5, 6]])
print('Here is a:')
print(a)
print('type(a): ', type(a))
print('rank of a: ', a.dim())
print('a.shape: ', a.shape)

torch.zeros(2, 3)
torch.ones(2, 3)
torch.eye(3)
torch.rand(2, 3)
torch.full((M, N), 3.14)

y2 = torch.tensor([1, 2], dtype=torch.int64)
print(y2.dtype)

x3 = x0.to(torch.float32)

x0 = torch.eye(3, dtype=torch.float64)  # Shape (3, 3), dtype torch.float64
x1 = torch.zeros_like(x0)               # Shape (3, 3), dtype torch.float64
x2 = x0.new_zeros(4, 5)                 # Shape (4, 5), dtype torch.float64
x3 = torch.ones(6, 7).to(x0)            # Shape (6, 7), dtype torch.float64
```

Even though PyTorch provides a large number of numeric datatypes, the most commonly used datatypes are:

- `torch.float32`: Standard floating-point type; used to store learnable parameters, network activations, etc. Nearly all arithmetic is done using this type.
- `torch.int64`: Typically used to store indices
- `torch.bool`: Stores boolean values: 0 is false and 1 is true
- `torch.float16`: Used for mixed-precision arithmetic, usually on NVIDIA GPUs with [tensor cores](https://www.nvidia.com/en-us/data-center/tensorcore/). You won't need to worry about this datatype in this course.
- 注意 `a[:, 1]` 和 `a[:, 1:2]` 的区别，后者会保留的多一点
- `clone()` 以后的变量跟原变量是独立的，但是等号直接赋值的是同一个指针

```python
mask = (a > 3)
print('\nMask tensor:')
print(mask)
# Mask tensor: tensor([[False, False], [False, True], [ True, True]])
```

- As its name implies, a tensor returned by `.view()` shares the same data as the input, so changes to one will affect the other.

??? reshape和view的区别 note
    1. **内存连续性**：
        - `view` 要求原始张量和目标张量在内存中是连续的。如果原始张量不是连续的， `view` 会首先调用 `contiguous` 方法使其连续，然后改变形状。如果张量已经是连续的， `view` 操作不会复制数据。
        - `reshape`不要求原始张量是连续的。如果原始张量不是连续的，`reshape`会创建一个新的张量并复制数据，以确保新张量是连续的。
    2. **返回值**
        - `view`返回一个新的张量，它与原始张量共享相同的数据，但是有不同的形状。如果原始张量不是连续的，`view`会返回一个副本。
        - `reshape`也返回一个新的张量，但总是创建数据的副本，即使原始张量是连续的。
    3. **使用场景**：
        - 当你确定原始张量是连续的，并且你想要避免不必要的数据复制时，可以使用`view`。
        - 当你不确定原始张量是否连续，或者你想要确保操作不会因非连续性而失败时，可以使用`reshape`。
    4. **参数**：
        - `view`的参数是目标形状的维度。
        - `reshape`的参数也是目标形状的维度，但它可以接受一个额外的参数`inplace`，如果设置为`True`，则会在原地修改张量的形状。

-  `torch.sin(x)` 和 `x.sin()` 是等价的

```python
x = torch.tensor([[1, 2, 3],
                  [4, 5, 6]], dtype=torch.float32)
print('Original tensor:')
print(x)

print('\nSum over entire tensor:')
print(torch.sum(x))
print(x.sum())
  
# We can sum over each row:
print('\nSum of each row:')
print(torch.sum(x, dim=0))
print(x.sum(dim=0))
  
# Sum over each column:
print('\nSum of each column:')
print(torch.sum(x, dim=1))
print(x.sum(dim=1))
```

- [`torch.dot`](https://pytorch.org/docs/stable/generated/torch.dot.html#torch.dot): Computes inner product of vectors
- [`torch.mm`](https://pytorch.org/docs/stable/generated/torch.mm.html#torch.mm): Computes matrix-matrix products
- [`torch.mv`](https://pytorch.org/docs/stable/generated/torch.mv.html#torch.mv): Computes matrix-vector products
- [`torch.addmm`](https://pytorch.org/docs/stable/generated/torch.addmm.html#torch.addmm) / [`torch.addmv`](https://pytorch.org/docs/stable/generated/torch.addmv.html#torch.addmv): Computes matrix-matrix and matrix-vector multiplications plus a bias
- [`torch.bmm`](https://pytorch.org/docs/stable/generated/torch.bmm.html#torch.bmm) / [`torch.baddmm`](https://pytorch.org/docs/stable/generated/torch.baddbmm.html#torch.baddbmm): Batched versions of `torch.mm` and `torch.addmm`, respectively
- [`torch.matmul`](https://pytorch.org/docs/stable/generated/torch.matmul.html#torch.matmul): General matrix product that performs different operations depending on the rank of the inputs. Confusingly, this is similar to `np.dot` in numpy.