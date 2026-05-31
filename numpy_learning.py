"""
NumPy Learning Script for Beginners.

Author: Chaitanya Dasadiya
GitHub: https://github.com/cdasadiya
LinkedIn: https://in.linkedin.com/in/chaitanya-dasadiya
"""

# Covers core NumPy concepts with simple examples and explanations

import numpy as np

# 1. Creating Arrays
arr1 = np.array([1, 2, 3, 4])
arr2 = np.array([[1, 2], [3, 4]])
zeros = np.zeros((2, 3))
ones = np.ones((2, 2))
arange = np.arange(0, 10, 2)
linspace = np.linspace(0, 1, 5)

print(f"arr1: {arr1}, arr2: {arr2}, zeros: {zeros}, ones: {ones}, arange: {arange}, linspace: {linspace}")

# 2. Array Properties
print(f"Shape of arr2: {arr2.shape}")
print(f"Size of arr2: {arr2.size}")
print(f"Data type of arr2: {arr2.dtype}")

# 3. Indexing and Slicing
print(f"First element of arr1: {arr1[0]}")
print(f"Slice of arr1: {arr1[1:3]}")
print(f"Element from 2D array: {arr2[1, 1]}")

# 4. Math Operations
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(f"a + b: {a + b}, a - b: {a - b}, a * b: {a * b}, a / b: {a / b}")

# 5. Aggregate Functions
print(f"Sum of a: {np.sum(a)}")
print(f"Mean of a: {np.mean(a)}")
print(f"Max of a: {np.max(a)}")
print(f"Min of a: {np.min(a)}")
print(f"Standard deviation of a: {np.std(a)}")

# 6. Reshape
arr = np.arange(6)
reshaped = arr.reshape((2, 3))
print(f"Reshaped array:\n{reshaped}")
print(f"Flattened array: {reshaped.flatten()}")

# 7. Random
print(f"Random floats:\n{np.random.rand(2, 2)}")
print(f"Random integers:\n{np.random.randint(1, 10, (2, 3))}")

# 8. Sorting
unsorted = np.array([3, 1, 2])
print(f"Sorted array: {np.sort(unsorted)}")

# 9. Combining Arrays
x = np.array([1, 2])
y = np.array([3, 4])
print(f"Concatenated array: {np.concatenate((x, y))}")
print(f"Vertically stacked arrays:\n{np.vstack((x, y))}")

# 10. Boolean Operations
arr = np.array([1, 2, 3, 4])
print(f"Condition (arr > 2): {arr > 2}")
print(f"Filtered array: {arr[arr > 2]}")

# 11. Broadcasting
print(f"Broadcasting result: {arr + 5}")

# 12. Copy vs View
original = np.array([1, 2, 3])
copy = original.copy()
view = original.view()
original[0] = 99

print(f"Original: {original}")
print(f"Copy: {copy}")
print(f"View: {view}")
