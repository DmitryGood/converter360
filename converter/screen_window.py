import numpy as np
import math
from Utils3D.Vector3D import Vector3D
from Utils3D.Screen3D import Screen3D, CylindricCoordinates
import cv2

# Events
def processMouseInput(event, x, y, flags, param):
    global view, flag_view_changed, size_x, size_y, cam_center, cam_radius

    if event == cv2.EVENT_LBUTTONDOWN:
        x = x / display_ratio
        y = y / display_ratiopython
        if x > 0 and x < size_x and y > 0 and y < size_y:
            rel_x = ( x - cam_center[0])
            r = math.sqrt( rel_x ** 2 + (y - cam_center[1]) ** 2)
            if y < cam_center[1]:
                phi = math.acos((- rel_x) / r)
            else:
                phi = math.pi * 2 - math.acos((- rel_x) / r)
            view['theta'] = math.acos( r / cam_radius) / math.pi * 180
            view['phi'] = phi / math.pi * 180
            flag_view_changed = True
            print "x: %s, y: %s, rel_x: %s, r: %s, phi: %s, theta: %s" %(x, y, rel_x, r, view['phi'], view['theta'])

# Main procedure
# open file
#img = cv2.imread('../img/balcony.jpg')
img = cv2.imread('../img/circle_4bf.jpg')
#img = cv2.imread('../img/down.jpg')
img_size = img.shape

# exit if wrong size
if (img.shape[0] % 2 != 0 or img.shape[1] % 2 != 0):
    print " Wrong size"
    exit()
# get left image params
size_x = img.shape[1] // 2
size_y = img.shape[0]
left_img = img[0 : size_y, 0 : size_x]

# camera parameters
cam_center = ( 786, 786)
cam_center_full = (( 786, 786), (732 + size_x, 770))
#cam_radius = 713
cam_radius = 664
display_ratio = 0.5

# Screen parameters
view = { 'dist' : cam_radius * math.cos(math.pi / 4), 'phi': 0, 'theta': 90}
screen_sizes = cam_radius / math.cos(math.pi / 4)
screen_size_width = int(screen_sizes)
screen_size_heigth = int(screen_sizes)
screen_horiz_resolution = int(screen_sizes / 2)
screen_vert_resolution = int(screen_sizes / 2)

scr = Screen3D(screen_size_width, screen_size_heigth, screen_horiz_resolution, screen_vert_resolution)
flag_view_changed = True

cv2.imshow("Left camera", left_img)

cv2.setMouseCallback("Left camera", processMouseInput)

while(True):
    # Redraw viewpoint if view changed
    if (flag_view_changed):
        cyl = CylindricCoordinates(view['dist'], view['phi'], view['theta'])
        #print "Coordinates: ", cyl
        scr.initScreen(cyl)
        rx, ry = scr.getResolution()
        temp_img = left_img.copy()

        #cam_img = scr.getHalfScreenImage(left_img, cam_center, cam_radius, temp_img)
        cam_img = scr.getFullScreenImage(img, cam_center_full, cam_radius, temp_img)

        # draw image
        small_img = cv2.resize(temp_img, None, fx = display_ratio, fy = display_ratio)
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
    elif c == ord('s'):     # implement hotkeys - center
        view['phi'] = 0
        view['theta'] = 90
        flag_view_changed = True
        print "Phi increased: ", view
    elif c == ord('a'):     # implement hotkeys - left
        view['phi'] = 0
        view['theta'] = 0
        flag_view_changed = True
        print "Phi increased: ", view
    elif c == ord('d'):     # implement hotkeys - right
        view['phi'] = 180
        view['theta'] = 0
        flag_view_changed = True
        print "Phi increased: ", view
    elif c == ord('w'):     # implement hotkeys - up
        view['phi'] = 90
        view['theta'] = 0
        flag_view_changed = True
        print "Phi increased: ", view
    elif c == ord('x'):     # implement hotkeys - down
        view['phi'] = 270
        view['theta'] = 0
        flag_view_changed = True
        print "Phi increased: ", view
    elif c == ord('p'):
        cam_radius += 1
        flag_view_changed = True
        print "Cam radius increased: %s", cam_radius
    elif c == ord('o'):
        cam_radius -= 1
        flag_view_changed = True
        print "Cam radius decreased: %s", cam_radius


