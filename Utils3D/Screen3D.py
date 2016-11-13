import math
import numpy as np
import cv2
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

    def getHalfScreenImage(self, cam_image, cam_center, cam_radius, temp_image = None, color=(0, 255, 0)):
        size_y, size_x, c = cam_image.shape

        cam_img = np.zeros((self.ry + 1, self.rx + 1, 3), dtype=cam_image.dtype)
        for x in range(0, self.rx + 1):
            for y in range(0, self.ry + 1):

                if (True):
                    # do only for canvas
                    v = self.get_screen_vector_by_coord(x, y)
                    cyl = self.get_cylindric_coordinates(v)
                    dist, phi, theta = cyl.getRadians()
                    # convert cylindric coordinates to camera coordinates
                    radius = (math.pi / 2 - theta) / (math.pi / 2) * cam_radius  # theta: 0 = center, pi/2 = edge
                    angle = phi + math.pi
                    cam_x = int(round(radius * math.cos(angle) + cam_center[0], 0))
                    cam_y = int(round(radius * math.sin(angle) + cam_center[1], 0))
                    if (cam_x < 0 or cam_x > size_x - 1 or cam_y < 0 or cam_y > size_y - 1):
                        continue
                    # print "Vector: %s, cyl: %s, cam: <%s, %s>, point: ( %s, %s)" % (v, cyl, radius, angle, cam_x, cam_y)
                    cam_img[y, x] = cam_image[cam_y, cam_x]
                    if (x == 0 or x == self.rx or y == 0 or y == self.ry):
                        if temp_image != None:
                            cv2.circle(temp_image, (cam_x, cam_y), 2, color, 2)
                    if (x == 0 and y==0) or (x==self.rx and y==self.ry):
                        print cyl.getDegrees()
        return cam_img


    def getFullScreenImage(self, cam_image, cam_center, cam_radius, temp_image=None, color=(0, 255, 0)):
        size_y, size_x, c = cam_image.shape
        size_half_x = size_x // 2

        cam_img = np.zeros((self.ry + 1, self.rx + 1, 3), dtype=cam_image.dtype)
        for x in range(0, self.rx + 1):
            for y in range(0, self.ry + 1):

                if (True):
                    # do only for canvas
                    v = self.get_screen_vector_by_coord(x, y)
                    cyl = self.get_cylindric_coordinates(v)
                    dist, phi, theta = cyl.getRadians()
                    if theta >=0:
                        # theta correction
                        gamma = 1.3
                        core = (math.pi / 2 - theta) / (math.pi / 2)
                        if core != 0:
                            core = 1 - (1 - core) ** gamma

                        # draw from the left image
                        radius = core * cam_radius  # theta: 0 = center, pi/2 = edge
                        angle = phi + math.pi
                        cam_x = int(round(radius * math.cos(angle) + cam_center[0][0], 0))
                        cam_y = int(round(radius * math.sin(angle) + cam_center[0][1], 0))
                        if (cam_x < 0 or cam_x > size_half_x - 1 or cam_y < 0 or cam_y > size_y - 1):
                            continue
                        # print "Vector: %s, cyl: %s, cam: <%s, %s>, point: ( %s, %s)" % (v, cyl, radius, angle, cam_x, cam_y)
                        cam_img[y, x] = cam_image[cam_y, cam_x]
                        if (x == 0 or x == self.rx or y == 0 or y == self.ry):
                            if temp_image != None:
                                cv2.circle(temp_image, (cam_x, cam_y), 2, color, 2)
                        if (x == 0 and y == 0) or (x == self.rx and y == self.ry):
                            pass
                            #print cyl.getDegrees()
                    else:   # Theta < 0
                        # draw from the right image
                        theta = abs(theta)
                        # theta correction
                        gamma = 1.3
                        core = (math.pi / 2 - theta) / (math.pi / 2)
                        if core != 0:
                            core = 1 - (1 - core) ** gamma
                        radius = core * cam_radius  # theta: 0 = center, pi/2 = edge
                        angle = phi
                        cam_x = int(round(radius * math.cos(angle) + cam_center[1][0], 0))
                        cam_y = int(round(cam_center[1][1] - radius * math.sin(angle), 0))
                        if (cam_x < size_half_x or cam_x > size_x - 1 or cam_y < 0 or cam_y > size_y - 1):
                            continue
                        # print "Vector: %s, cyl: %s, cam: <%s, %s>, point: ( %s, %s)" % (v, cyl, radius, angle, cam_x, cam_y)
                        cam_img[y, x] = cam_image[cam_y, cam_x]
                        if (x == 0 or x == self.rx or y == 0 or y == self.ry):
                            if temp_image != None:
                                cv2.circle(temp_image, (cam_x, cam_y), 2, color, 2)
                        if (x == 0 and y == 0) or (x == self.rx and y == self.ry):
                            pass
                            #print cyl.getDegrees()
        return cam_img
