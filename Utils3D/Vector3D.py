import math

#   Class for handling 3D vector operations

class Vector3D:

    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    # Test equal
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    # String represntation
    def __str__(self):
        return '<%s, %s, %s>' % (self.x, self.y, self.z)

    # Produce a copy of itself
    def __copy(self):
        return Vector3D(self.x, self.y, self.z)

    # Negative
    def __neg__(self):
        return Vector3D(-self.x, -self.y, -self.z)

    # Multiplications: vector over scalar or scalar of two vectors
    def __mul__(self, operand):
        # Multiplication of vector over scalar
        if type(operand) == type(1) or type(operand) == type(1.0):
            return Vector3D(self.x * operand, self.y * operand, self.z * operand)
        # Scalar multiplication of two vectors
        elif type(operand) == type(self):
            return self.x * operand.x + self.y * operand.y + self.z * operand.z

    def __rmul__(self, number):
        return self.__mul__(number)

    # Division
    def __div__(self, number):
        # Return only if number
        if ( type(number) == type(1) or type(number) == type(1.0))  and number != 0:
            return self.__copy() * ( number ** -1)
        return None

    # Arithmetic Operations
    def __add__(self, operand):
        return Vector3D(self.x + operand.x, self.y + operand.y, self.z + operand.z)

    def __sub__(self, operand):
        return self.__copy() + -operand

    # Cross product
    # cross = a ** b
    # vector multiplication
    def __pow__(self, operand):
        return Vector3D(self.y * operand.z - self.z * operand.y,
                        self.z * operand.x - self.x * operand.z,
                        self.x * operand.y - self.y * operand.x)

    # Dot Project
    # dp = a & b
    def __and__(self, operand):
        return (self.x * operand.x) + \
               (self.y * operand.y) + \
               (self.z * operand.z)

    # Operations

    def normal(self):
        mag = self.magnitude()
        if mag == 0:
            return 0
        else:
            return self.__copy() / mag

    # Length
    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
