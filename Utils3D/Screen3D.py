import math
from Utils3D.Vector3D import Vector3D

def degToRad(deg):
    return float(deg) * math.pi / 180.0


def radToDeg(rad):
    return rad / math.pi * 180.0

class CylindricCoordinates():
    def __init__(self, dist, phi, theta):
        self.dist = float(dist)
        self.phi = float(phi)
        self.theta = float(theta)

    def getDegrees(self):
        return (self.dist, self.phi, self.theta)

    def getRadians(self):
        return (self.dist, degToRad(self.phi), degToRad(self.theta))

    def __str__(self):
        return "{ d: %3.3s, phi: %3.3s, theta: %3.3s}" %(self.dist, self. phi, self.theta)

# class for handling 3D screen operations screen
class Screen3D():
    def __init__(self, width, height, resolution_x, resolution_y):
        self.width = width
        self.height = height
        self.rx = resolution_x
        self.ry = resolution_y

    def getResolution(self):
        return (self.rx, self.ry)

    def initScreen(self, cylindric):
        dist, phi, theta = cylindric.getRadians()
        # Old functions
        #self.A = dist * math.sin(theta) * math.cos(phi)
        #self.B = dist * math.sin(theta) * math.sin(phi)
        #self.C = round(dist * math.cos(theta), 6)
        # New functions
        self.A = round ( dist * math.sin(theta), 6)
        self.B = round ( dist * math.cos(theta) * math.cos(phi), 6)
        self.C = round ( dist * math.cos(theta) * math.sin(phi), 6)

        self.normal = Vector3D(self.A, self.B, self.C)
        if (self.A == 0 and self.B == 0):
            th_sign = (theta - math.pi) / abs( theta - math.pi)
            self.vector_h = Vector3D(0, th_sign, 0).normal()
        else:
            self.vector_h = Vector3D(self.B, -self.A, 0).normal()
        self.vector_v = (self.normal ** self.vector_h).normal()

    def get_screen_vector_by_coord(self, x, y):
        screen_x = float(self.width) * ( x - self.rx / 2) / self.rx
        screen_y = float(self.height) * ( y - self.ry / 2) / self.ry
        screen_vect = self.vector_h * screen_x + self.vector_v * screen_y
        return self.normal + screen_vect

    def get_cylindric_coordinates(self, vector):
        dist = vector.magnitude()
        # Old functions
        #phi = math.acos(( vector.x / math.sqrt( vector.x ** 2 + vector.y ** 2)))
        #theta = math.acos((vector.z / dist))
        # new functions
        if ( vector.z == 0 and vector.y == 0):
            phi = 0
        elif ( vector.z >= 0):
            phi = math.acos((vector.y / math.sqrt(vector.y ** 2 + vector.z ** 2)))
        else:
            phi = math.pi* 2 - math.acos((vector.y / math.sqrt(vector.y ** 2 + vector.z ** 2)))
        theta = math.asin((vector.x / dist))

        return CylindricCoordinates(dist, radToDeg(phi), radToDeg(theta))

