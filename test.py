import math
import numpy as np


a = np.array([[1, 2, 3]])
print(a.shape)
print(a.squeeze().shape)

b = np.array([[1.]])
print(b, b.shape)
b_squeeze = b.squeeze()
print(b_squeeze, b_squeeze.shape, type(b_squeeze))
b_tolist = b_squeeze.tolist()
print(b_tolist, type(b_tolist))

for i in range(9):
    print("\n\n", i+1)
    x = np.arange(1, i+2, 1)
    iteration = 0
    while len(x) < 8:
        iteration += 1
        print("Iteratino:", iteration)
        x = np.append(x, 0)
    print(x)
