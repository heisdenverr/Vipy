class Vipy:
    def __init__(self, data):
        self.data = data
        self.shape = (len(data), len(data[0]) if data and isinstance(data[0], list) else 1)

    def __getitem__(self, index):
        return self.data[index]

    def __repr__(self):
        return f"Vipy array({self.data})"

    @staticmethod
    def toarray(data):
        if data == 1:
            return Vipy.toarray(list(data))
        else:
            return Vipy(data)

    def add(self, other):
        if self.shape != other.shape:
            raise ValueError("Shapes do not match for element-wise addition")
        return Vipy([[self.data[i][j] + other.data[i][j] for j in range(len(self.data[0]))] for i in range(len(self.data))])

    def mul(self, other):
        if self.shape != other.shape:
            raise ValueError("Shapes do not match for element-wise multiplication")
        return Vipy([[self.data[i][j] * other.data[i][j] for j in range(len(self.data[0]))] for i in range(len(self.data))])

    def __add__(self, other):
        return self.add(other)

    def __mul__(self, other):
        return self.mul(other)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)
    
    def __lt__(self, other):
        return Vipy([[1 if self.data[i][j] < other else 0 for j in range(len(self.data[0]))] for i in range(len(self.data))])

    def __le__(self, other):
        return Vipy([[1 if self.data[i][j] <= other else 0 for j in range(len(self.data[0]))] for i in range(len(self.data))])

    def __gt__(self, other):
        return Vipy([[1 if self.data[i][j] > other else 0 for j in range(len(self.data[0]))] for i in range(len(self.data))])

    def __ge__(self, other):
        return Vipy([[1 if self.data[i][j] >= other else 0 for j in range(len(self.data[0]))] for i in range(len(self.data))])

class Engine:
    def __init__(self, data, children=(), _ops=" "):
        self.data = data
        self._prev = set(children)
        self._ops = _ops
        self.grad = 0  # Initialize gradient as an integer
        self._backward = lambda: None

    def __repr__(self):
        return f"Engine (data={self.data.data})"

    def __add__(self, other):
        other = other if isinstance(other, Engine) else Engine(Vipy.toarray(other))
        out = Engine(self.data.add(other.data), (self, other), '+')

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward

        return out

    def __mul__(self, other):
        other = other if isinstance(other, Engine) else Engine(Vipy.toarray(other))
        out = Engine(self.data.mul(other.data), (self, other), '*')

        def _backward():
            self.grad += sum(sum(row) for row in other.data.data) * out.grad
            other.grad += sum(sum(row) for row in self.data.data) * out.grad
        out._backward = _backward

        return out
    
    def ReLU(self):
        out = Engine((self.data > 0).mul(self.data), (self,), 'ReLU')

        def _backward():
            oth = out if isinstance(out, Engine) else Engine(out)
            self.grad += Engine((oth.data > 0) * Vipy.toarray(oth.grad))
        out._backward = _backward

        return out


    def backward(self):
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)

        self.grad = 1  # Start the backpropagation with gradient 1
        for node in reversed(topo):
            node._backward()

# Example usage
a = [[0, 1], [1, 0]]
b = [[3, 4], [1, 2]]

engine_a = Engine(Vipy.toarray(a))
engine_b = Engine(Vipy.toarray(b))

# Example of addition
result_add = (engine_a + engine_b).ReLU()
result_add.backward()

print("Result of addition:")
print(result_add.data)
print("Gradient after addition:")
print(engine_a.grad)
print(engine_b.grad)

# Example of multiplication
result_mul = engine_a * engine_b
result_mul.backward()

print("\nResult of multiplication:")
print(result_mul.data)
print("Gradient after multiplication:")
print(engine_a.grad)
print(engine_b.grad)