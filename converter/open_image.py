import cv2
img = cv2.imread('../img/balcony.jpg')
img_size = img.shape

x=500
y=400
w=600
h=400
step = 5

prev_char = -1

while(True):
    c = cv2.waitKey(1)

    if c == 27:
        break
    if c == ord('l'):           # right
        if ( x + w < img_size[1] - step):
            x += step
        else:
            x = img_size[1] - w
    elif c == ord('j'):         # left
        if ( x  > step):
            x -= step
        else:
            x = 0
    elif c == ord('i'):         # up
        if ( y  > step):
            y -= step
        else:
            y = 0
    elif c == ord('k'):         # down
        if ( y + h < img_size[0] - step):
            y += step
        else:
            y = img_size[0] - h


    part = img[y : y + h, x : x + w]
    cv2.imshow('Input image', part)

#part = img[500:900,500:600]
#cv2.imshow('Input image', part)
#cv2.waitKey()
cv2.imwrite("../out/test.jpg", part)
cv2.destroyAllWindows()