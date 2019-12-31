import cv2
import numpy as np

# Sides to detail
# GREEN = SIDE
# RED = OUTER
# BLUE = INNER

# Quickly save an image to gray scale
img_c = cv2.imread('jigsaw_temp_imgs/cropped.png')
img_c = cv2.resize(img_c, None, fx=0.80, fy=0.80)  # resize since image is huge
img_c = cv2.cvtColor(img_c, cv2.COLOR_BGR2GRAY)
cv2.imwrite('temp.png', img_c
            )
# Load the gray scale back up
original = img_c = cv2.imread('temp.png')


def locate_side_pieces():
    for file_number in range(0, 13, 1):
        filename = '../pieces/test_full_JIGSAW_PIECE_{}.png'.format(file_number)
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 75, 150)

        try:
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, minLineLength=65, maxLineGap=10)

            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.line(original, (x1, y1), (x2, y2), (0, 255, 0), 1)

                print(((x2 - x1)**2 + (y2 - y1)**2)**.5)

            cv2.imshow("linesDetected", img)
            print(filename, len(lines))
            cv2.waitKey(1)

        except:
            print('Not Side / Corner piece')
            filename = '../pieces/test_full_JIGSAW_PIECE_{}.png'.format(file_number)
            img = cv2.imread(filename)
            cv2.imshow("linesDetected", img)
            cv2.waitKey(1)

    cv2.imwrite('linesHoughCropped.png', original)
    cv2.imshow("linesDetected", original)
    cv2.waitKey(0)


def locate_outter():
    for file_number in range(0, 13, 1):
        filename = '../pieces/test_full_JIGSAW_PIECE_{}.png'.format(file_number)
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 75, 150)

        try:
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, minLineLength=65, maxLineGap=10)
            #lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, minLineLength=65, maxLineGap=10)

            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.line(original, (x1, y1), (x2, y2), (0, 255, 0), 1)

                print(((x2 - x1)**2 + (y2 - y1)**2)**.5)

            cv2.imshow("linesDetected", img)
            print(filename, len(lines))
            cv2.waitKey(0)

        except:
            print('Not Side / Corner piece')
            filename = '../pieces/test_full_JIGSAW_PIECE_{}.png'.format(file_number)
            img = cv2.imread(filename)
            cv2.imshow("linesDetected", img)
            cv2.waitKey(1)

    cv2.imwrite('linesHoughCropped.png', original)
    cv2.imshow("linesDetected", original)
    cv2.waitKey(0)


locate_outter()