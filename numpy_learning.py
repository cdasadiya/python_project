# NumPy Learning Script for Beginners
# Covers core NumPy concepts with simple examples and explanations

import numpy as np

# 1. Creating Arrays
arr1 = np.array([1, 2, 3, 4])  # create array from list
arr2 = np.array([[1, 2], [3, 4]])  # 2D array
zeros = np.zeros((2, 3))  # array of zeros
ones = np.ones((2, 2))  # array of ones
arange = np.arange(0, 10, 2)  # range with step
linspace = np.linspace(0, 1, 5)  # evenly spaced numbers

print(arr1, arr2, zeros, ones, arange, linspace)

# 2. Array Properties
print(arr2.shape)  # shape (rows, cols)
print(arr2.size)   # total elements
print(arr2.dtype)  # data type

# 3. Indexing and Slicing
print(arr1[0])     # first element
print(arr1[1:3])   # slice
print(arr2[1, 1])  # element from 2D array

# 4. Math Operations
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(a + b, a - b, a * b, a / b)  # basic math

# 5. Aggregate Functions
print(np.sum(a))
print(np.mean(a))
print(np.max(a))
print(np.min(a))
print(np.std(a))

# 6. Reshape
arr = np.arange(6)
reshaped = arr.reshape((2, 3))
print(reshaped)
print(reshaped.flatten())  # flatten to 1D

# 7. Random
print(np.random.rand(2, 2))  # random floats
print(np.random.randint(1, 10, (2, 3)))  # random integers

# 8. Sorting
unsorted = np.array([3, 1, 2])
print(np.sort(unsorted))

# 9. Combining Arrays
x = np.array([1, 2])
y = np.array([3, 4])
print(np.concatenate((x, y)))
print(np.vstack((x, y)))

# 10. Boolean Operations
arr = np.array([1, 2, 3, 4])
print(arr > 2)  # condition
print(arr[arr > 2])  # filtering

# 11. Broadcasting
print(arr + 5)  # add scalar to all elements

# 12. Copy vs View
original = np.array([1, 2, 3])
copy = original.copy()  # separate copy
view = original.view()  # linked view
original[0] = 99

print(original)
print(copy)
print(view)
