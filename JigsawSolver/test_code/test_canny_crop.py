import cv2
import numpy as np

crop_rect_dict = {}
crop_shape_dict = {}


def static_crop_shape(pic, crop_out=False, save=True):
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
    # Tested with [CHAIN_APPROX_SIMPLE, CHAIN_APPROX_NONE, CHAIN_APPROX_TC89_L1, CHAIN_APPROX_TC89_KCOS]
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # Iterate thorugh contours and filter for ROI
    image_number = 0

    #_, contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    img2 = cv2.imread(pic, 0)
    img2 = cv2.resize(img2, None, fx=0.80, fy=0.80) # resize since image is huge

    # https://stackoverflow.com/questions/28759253/how-to-crop-the-internal-area-of-a-contour
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        epsilon = 0.000001 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)

        rsz_img = cv2.drawContours(rsz_img, [approx], 0, (0,255,0), 2)

        if crop_out:
            ROI = original[y:y+h, x:x+w]
            crop_shape_dict["JIGSAW_PIECE_{}.png".format(image_number)] = ROI

            mask = np.zeros_like(img2) # Create mask where white is what we want, black otherwise
            cv2.drawContours(mask, cnts, image_number, 255, 0) # Draw filled contour in mask

            out = np.zeros_like(img2) # Extract out the object and place into output image
            out[mask == 255] = img2[mask == 255]

            # Now crop
            (y, x) = np.where(mask == 255)
            (topy, topx) = (np.min(y), np.min(x))
            (bottomy, bottomx) = (np.max(y), np.max(x))
            out = out[topy:bottomy+1, topx:bottomx+1]

            crop_shape_dict["test_JIGSAW_PIECE_{}.png".format(image_number)] = out

            image_number += 1

    if save:

        for crop in crop_shape_dict:
            cv2.imwrite(crop, crop_shape_dict[crop])

        for crop in crop_rect_dict:
            cv2.imwrite(crop, crop_rect_dict[crop])


    cv2.imshow('canny', canny)
    cv2.imshow('image', rsz_img)
    cv2.waitKey(0)


def filter_jigsaw_pieces(a):
    return a

static_crop_shape('cropped.png', crop_out=True, save=True)
