import math
from Utils3D.Screen3D import Screen3D, CylindricCoordinates
import cv2




# Main procedure
# open file
img = cv2.imread('../img/balcony.jpg')
#img = cv2.imread('../img/circle_4bf.jpg')
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

# Redraw viewpoint if view changed
cyl = CylindricCoordinates(view['dist'], 0, 90)
scr.initScreen(cyl)
#rx, ry = scr.getResolution()
cam_img_center = scr.getFullScreenImage(img, cam_center_full, cam_radius)
print "Center"

# Top
scr.initScreen(CylindricCoordinates(view['dist'], 90, 0))
cam_img_top = scr.getFullScreenImage(img, cam_center_full, cam_radius)
print "Top"

# Right
scr.initScreen(CylindricCoordinates(view['dist'], 180, 0))
cam_img_right = scr.getFullScreenImage(img, cam_center_full, cam_radius)
print "Right"

# Left
scr.initScreen(CylindricCoordinates(view['dist'], 0, 0))
cam_img_left = scr.getFullScreenImage(img, cam_center_full, cam_radius)
print "Left"

# Bottom
scr.initScreen(CylindricCoordinates(view['dist'], 270, 0))
cam_img_bottom = scr.getFullScreenImage(img, cam_center_full, cam_radius)
print "Bottom"

# Back
scr.initScreen(CylindricCoordinates(view['dist'], 0, -90))
cam_img_back = scr.getFullScreenImage(img, cam_center_full, cam_radius)
print "Back"


# draw image
#small_img = cv2.resize(temp_img, None, fx = display_ratio, fy = display_ratio)
#cv2.imshow("Left camera", small_img)
print "Draw images"
cv2.imshow("Camera image - Center", cam_img_center)
cv2.imshow("Camera image - Top", cam_img_top)
cv2.imshow("Camera image - Right", cam_img_right)
cv2.imshow("Camera image - Left", cam_img_left)
cv2.imshow("Camera image - Bottom", cam_img_bottom)
cv2.imshow("Camera image - Back", cam_img_back)

cv2.waitKey()

directory = "../out/"
file_prefix = "balcony_"

print "Write: ", directory + file_prefix + "center" + ".jpg"
cv2.imwrite(directory + file_prefix + "center" + ".jpg", cam_img_center)
cv2.imwrite(directory + file_prefix + "top" + ".jpg", cam_img_top)
cv2.imwrite(directory + file_prefix + "right" + ".jpg", cam_img_right)
cv2.imwrite(directory + file_prefix + "left" + ".jpg", cam_img_left)
cv2.imwrite(directory + file_prefix + "bottom" + ".jpg", cam_img_bottom)
cv2.imwrite(directory + file_prefix + "back" + ".jpg", cam_img_back)

cv2.destroyAllWindows()