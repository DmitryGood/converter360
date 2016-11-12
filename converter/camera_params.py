import cv2
img = cv2.imread('../img/balcony.jpg')
img_size = img.shape

# exit if wrong size
if (img.shape[0] % 2 != 0 or img.shape[1] % 2 != 0):
    print " Wrong size"
    exit()

size_x = img.shape[1] // 2
size_y = img.shape[0]
radius = size_x // 2
color = (0, 255, 0)
x = size_x // 2
y = size_y // 2
left_img = img[0 : size_y, 0 : size_x]
right_img = img[0 : size_y, size_x : size_x * 2]

right_small = cv2.resize(right_img, None, fx=0.25, fy=0.25)
cv2.imshow("Right image", right_small)

while (True):

    part = left_img.copy()
    cv2.circle(part, (x, y), radius, color, thickness=2)
    text = " %s, %s, %s" % (x, y, radius)
    #print text
    #cv2.putText(part, text, (50, 100), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 255))
    small = cv2.resize(part, None, fx=0.25, fy=0.25)
    cv2.putText(small, text, (-5, 15), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255))

    cv2.imshow('Left image', small)

    # Keyboard input
    c = cv2.waitKey(1)
    if c == 27:
        break
    if c == ord('l'):  # right
        x += 1
    elif c == ord('j'):  # left
        x -= 1
    elif c == ord('i'):  # up
        y -= 1
    elif c == ord('k'):  # down
        y += 1
    elif c == ord('q'):     # circle bigger
        radius += 1
    elif c == ord('a'):     # circle smaller
        radius -= 1



