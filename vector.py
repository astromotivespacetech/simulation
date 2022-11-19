import math


class Vector(object):

    def __init__(self, *args):
        if len(args) == 0:
            self.data = [0,0,0]
        elif len(args) == 1:
            self.data = args[0]
        elif len(args) == 2:
            self.data = [args[0], args[1], 0]
        elif len(args) == 3:
            self.data = [args[0], args[1], args[2]]
        self.x      = self.data[0]
        self.y      = self.data[1]
        self.z      = self.data[2]


    def sum(self, vector):
        new = [x+y for x, y in zip(self.data, vector.data)]
        return Vector(new)


    def difference(self, vector):
        new = [x-y for x, y in zip(self.data, vector.data)]
        return Vector(new)


    def add(self, vector):
        for i, x in enumerate(vector.data):
            self.data[i] += x
        self.__init__(self.data)


    def subtract(self, vector):
        for i, x in enumerate(vector.data):
            self.data[i] -= x
        self.__init__(self.data)

    def mult(self, scalar):
        new = [x*scalar for x in self.data]
        return Vector(new)


    def scale(self, scalar):
        for x in range(len(self.data)):
            self.data[x] *= scalar
        self.__init__(self.data)


    def divide(self, scalar):
        for x in range(len(self.data)):
            self.data[x] /= scalar
        self.__init__(self.data)


    def dot(self, vector):
        new = sum([x*y for x, y in zip(self.data, vector.data)])
        return new



    def cross(self, vector):
        x = self.y * vector.z - self.z * vector.y
        y = self.z * vector.x - self.x * vector.z
        z = self.x * vector.y - self.y * vector.x
        return Vector([x,y,z])


    def copy(self):
        return Vector(self.data)


    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)


    def unit(self):
        m = self.magnitude()
        if m == 0:
            new = [0, 0, 0]
        else:
            new = [1/m * self.x, 1/m * self.y, 1/m * self.z]
        return Vector(new)


    def inverse(self):
        new = [-1 * x for x in self.data]
        self.__init__(new)


    def angle(self, vector):
        m1      = self.magnitude()
        m2      = vector.magnitude()
        dot     = self.dot(vector)

        if dot / (m1 * m2) > 1.0:
            n   = 1.0
        elif dot / (m1 * m2) < -1.0:
            n   = -1.0
        else:
            n   = dot / (m1 * m2)
        return math.acos(n)


    def rotate(self, axis, angle):
        vrot = self.mult(math.cos(angle))
        v2 = axis.cross(self)
        v2 = v2.mult(math.sin(angle))
        v3 = axis.mult(axis.dot(self))
        v3 = v3.mult(1 - math.cos(angle))
        vrot.add(v2)
        vrot.add(v3)
        self.__init__(vrot.data)



    def update(self, array):
        self.__init__(array)
