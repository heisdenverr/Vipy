from main import Vipy as v

a = v([[0, 1],
      [1, 0]])

b = v([[3, 4],
      [1, 2]])
c = v([[1, 2],
       [3, 4],
       [9, 0]
       ]).T
print(a.add(b))
print(a.matmul(b))
print(a.T)
print(a.dot(b))