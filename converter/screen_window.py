import numpy as np
import math
from Utils3D.Vector3D import Vector3D
from Utils3D.Screen3D import Screen3D, CylindricCoordinates
import cv2

# Main procedure
# open file
img = cv2.imread('../img/balcony.jpg')
img_size = img.shape

# exit if wrong size
if (img.shape[0] % 2 != 0 or img.shape[1] % 2 != 0):
    print " Wrong size"
    exit()
# get left image params
size_x = img.shape[1] // 2
size_y = img.shape[0]
color = (0, 255, 0)
left_img = img[0 : size_y, 0 : size_x]

# camera parameters
cam_center = ( 786, 786)
cam_radius = 713

# Screen parameters
view = { 'dist' : 900, 'phi': 0, 'theta': 90}
screen_size_width = 500
screen_size_heigth = 500
screen_horiz_resolution = 400
screen_vert_resolution = 300

scr = Screen3D(screen_size_width, screen_size_heigth, screen_horiz_resolution, screen_vert_resolution)
flag_view_changed = True
while(True):
    # Redraw viewpoint if view changed
    if (flag_view_changed):
        cyl = CylindricCoordinates(view['dist'], view['phi'], view['theta'])
        #print "Coordinates: ", cyl
        scr.initScreen(cyl)
        rx, ry = scr.getResolution()
        temp_img = left_img.copy()
        cam_img = np.zeros((ry+1, rx+1, 3), dtype=left_img.dtype)
        for x in range(0, rx+1):
            for y in range(0, ry+1):

                if (True):
                    # do only for canvas
                    v = scr.get_screen_vector_by_coord(x, y)
                    cyl = scr.get_cylindric_coordinates(v)
                    dist, phi, theta = cyl.getRadians()
                    # convert cylindric coordinates to camera coordinates
                    radius = ( math.pi/2 - theta ) / (math.pi/2) * cam_radius  # theta: 0 = center, pi/2 = edge
                    angle = phi + math.pi
                    cam_x = int ( round( radius * math.cos(angle) + cam_center[0], 0))
                    cam_y = int ( round( radius * math.sin(angle) + cam_center[1], 0))
                    if ( cam_x < 0 or cam_x > size_x-1 or cam_y < 0 or cam_y > size_y-1):
                        continue
                    #print "Vector: %s, cyl: %s, cam: <%s, %s>, point: ( %s, %s)" % (v, cyl, radius, angle, cam_x, cam_y)
                    cam_img[ y, x ] = left_img [ cam_y, cam_x]
                    if (x == 0 or x == rx or y == 0 or y == ry):
                        cv2.circle(temp_img, (cam_x, cam_y), 2, color, 2)
        # draw image
        small_img = cv2.resize(temp_img, None, fx = 0.5, fy = 0.5)
        cv2.imshow("Left camera", small_img)
        cv2.imshow("Camera image", cam_img)
        flag_view_changed = False

    # Keyboard input
    c = cv2.waitKey(1)
    if c == 27:
        break
    elif c == ord('i') and view['theta'] !=0:  # from center
        view['theta'] -= 5
        if view['theta'] < 0:
            view['theta'] = 0
        flag_view_changed = True
        print "Theta decreased: ", view
    elif c == ord('k'):  # to center
        view['theta'] += 5
        if view['theta'] > 90:
            view['theta'] = 90
        flag_view_changed = True
        print "Theta increased: ", view
    elif c == ord('l') and view['phi'] > 5:  # rotate
        view['phi'] -= 5
        flag_view_changed = True
        print "Phi decreased: ", view
    elif c == ord('j')  and view['phi'] < 360:  # down
        view['phi'] += 5
        flag_view_changed = True
        print "Phi increased: ", view
    elif c == ord('q'):     # circle bigger
        pass
    elif c == ord('a'):     # circle smaller
        pass


