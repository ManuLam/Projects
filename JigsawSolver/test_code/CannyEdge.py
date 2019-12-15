import cv2
import numpy as np
from matplotlib import pyplot as plt


def static(image, show=False):
    img = cv2.imread(image,0)
    edges = cv2.Canny(img, 100, 200)

    plt.subplot(121),plt.imshow(img, cmap='gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])

    plt.subplot(122),plt.imshow(edges, cmap='gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    #im.show(edges)
    if show:
        plt.show()


# Real time camera
def dynamic():
    cap = cv2.VideoCapture(0)
    camera = 'dynamic.jpg'

    while 1:
        # Capture frame-by-frames
        ret, frame = cap.read()

        cv2.imwrite(camera, frame)  # save image
        img = cv2.imread(camera, 0)
        edges = cv2.Canny(img, 100, 200)

        cv2.imshow('test', edges)
        cv2.waitKey(1)


# Image uploaded crop pieces to rectangle
def static_crop_rec(pic, crop_out=False):
    # load image
    img = cv2.imread(pic)
    rsz_img = cv2.resize(img, None, fx=0.80, fy=0.80)  # resize since image is huge

    original = rsz_img.copy()
    gray = cv2.cvtColor(rsz_img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 120, 255, 1)
    kernel = np.ones((5,5),np.uint8)
    dilate = cv2.dilate(canny, kernel, iterations=1)

    # Find contours
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # Iterate thorugh contours and filter for ROI
    image_number = 0

    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(rsz_img, (x, y), (x + w, y + h), (36, 255, 12), 2)
        if crop_out:
            ROI = original[y:y+h, x:x+w]
            cv2.imwrite("ROI_RECT_{}.png".format(image_number), ROI)
            image_number += 1

    cv2.imshow('canny', canny)
    cv2.imshow('image', rsz_img)
    cv2.waitKey(0)


def static_crop_shape(pic, crop_out=False):
    # load image
    img = cv2.imread(pic)
    rsz_img = cv2.resize(img, None, fx=0.80, fy=0.80) # resize since image is huge

    original = rsz_img.copy()
    gray = cv2.cvtColor(rsz_img, cv2.COLOR_BGR2GRAY)

    # Blurring with gaussian for better contours
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 50, 255, 1)

    kernel = np.ones((5,5), np.uint8)
    dilate = cv2.dilate(canny, kernel, iterations=1)

    # Find contours
    # Todo CHAIN_APPROX_SIMPLE try different contours
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # Iterate thorugh contours and filter for ROI
    image_number = 0

    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        epsilon = 0.000001 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)

        rsz_img = cv2.drawContours(rsz_img, [approx], 0, (0,255,0), 2)

        if crop_out and (w > 100 and h > 100):
            ROI = original[y:y+h, x:x+w]
            cv2.imwrite("JIGSAW_PIECE_{}.png".format(image_number), ROI)

            image_number += 1

            # threshold input image using otsu thresholding as mask and refine with morphology
            ret, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            kernel = np.ones((1,1), np.uint8)

            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

            # put thresh into
            result = rsz_img.copy()
            result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
            result[:, :, 3] = mask

            # save resulting masked image
            cv2.imwrite('retina_masked.png', result)

    cv2.imshow('canny', canny)
    cv2.imshow('image', rsz_img)
    cv2.waitKey(0)


def test_code_mask(pic):
    # load image as grayscale
    img = cv2.imread(pic)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('test', gray)
    cv2.waitKey(0)
    # threshold input image using otsu thresholding as mask and refine with morphology
    ret, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    kernel = np.ones((9,9), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # put thresh into
    result = img.copy()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask

    # save resulting masked image
    cv2.imwrite('retina_masked.png', result)


original_image = 'jigsaw_image_3.jpg'

#test_static_crop_rec('cropped.png', crop_out=True)
static_crop_shape('cropped.png', crop_out=True)

#test_code_mask('cropped.png')
