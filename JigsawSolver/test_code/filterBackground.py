import cv2
import numpy as np
from PIL import Image

def filter_white_background(img):
    ## (1) Convert to gray, and threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    ## (2) Morph-op to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

    ## (3) Find the max-area contour
    cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnt = sorted(cnts, key=cv2.contourArea)[-1]

    ## (4) Crop and save it
    x,y,w,h = cv2.boundingRect(cnt)
    dst = img[y:y+h, x:x+w]
    cv2.imwrite("001.png", dst)


def filter_background():
    img = Image.open('JIGSAW_PIECE_0.png')
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            if item[0] > 200:
                newData.append((0, 0, 0, 255))
            else:
                newData.append(item)
                print(item)


    img.putdata(newData)
    img.save("open_science_logo_transparent.png", "PNG")

filter_white_background(cv2.imread("JIGSAW_PIECE_0.png"))
filter_background()