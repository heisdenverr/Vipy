class Vipy:

    def __init__(self, data: list):
        self.data = data
        self.shape = (len(data), len(data[0]) if data and isinstance(data[0], list) else 1)


    def __getiten__(self, index):
        return self.data[index]

    def __repr__(self):
        return f"Vipy array({self.data})"

    def add(self, other):
        if not isinstance(other, Vipy):
            raise ValueError("The operand must be an instance of MyArray")
        if self.shape != other.shape:
            raise ValueError("Shapes do not match for element-wise addition")
        return Vipy([[self.data[i][j] + other.data[i][j] for j in range(len(self.data[0]))] for i in range(len(self.data))])

    def matmul(self, other):
        if not isinstance(other, Vipy):
            raise ValueError("The operand must be an instance of MyArray")
        if self.shape[1] != other.shape[0]:
            raise ValueError("Shapes do not match for matrix multiplication")
        result = [[sum(self.data[i][k] * other.data[k][j] for k in range(self.shape[1])) for j in range(other.shape[1])] for i in range(self.shape[0])]
        return Vipy(result)
    
    def T(self):
        transposed = [[self.data[j][i] for j in range(len(self.data))] for i in range(len(self.data[0]))]
        return Vipy(transposed)

    # def dot(self, other):
    #     if self.shape == (len(self.data),):
    #         if len(self.data) != len(other.data):
    #             raise ValueError("Shapes do not match for dot product")
    #         return sum(self.data[i] * other.data[i] for i in range(len(self.data)))
    #     elif (len(self.data[0]) != len(other.data[0])):
    #         raise ValueError(f"Cannot do the dot product for array with shape: ({len(self.data)},{len(self.data[0])}),({len(other.data)},{len(other.data[0])})")
    #     else:
    #         return self.matmul(other)

    def dot(self, other):
        if not isinstance(other, Vipy):
            raise ValueError("The operand must be an instance of Vipy")
        if len(self.shape) == 1 and len(other.shape) == 1:
            # Both are 1D arrays
            if len(self.data) != len(other.data):
                raise ValueError("Shapes do not match for dot product")
            return sum(self.data[i] * other.data[i] for i in range(len(self.data)))
        elif self.shape[1] == other.shape[0]:
            # Matrix multiplication
            return self.matmul(other)
        else:
            raise ValueError("Shapes do not match for dot product")