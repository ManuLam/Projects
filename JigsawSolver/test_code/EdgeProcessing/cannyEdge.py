import logging

import cv2
import numpy as np

import ColoredFormatter
from JigsawSolver.test_code.EdgeProcessing.global_config import NORMAL_JIGSAW_PATH, NORMAL_JIGASW_PIECE, \
    CANNY_JIGSAW_PATH, CANNY_JIGASW_PIECE, FULL_JIGSAW_IMAGE, FULL_IMAGE_CANNY_JIGSAW_PATH, \
    FULL_IMAGE_CANNY_JIGASW_PIECE, JUNK_PIECES, FILTERED_JUNK_PATH

crop_rect_dict = {}
crop_shape_dict = {}

logger = logging.getLogger(__name__)


# Filter jigsaw pieces smaller than 15 pixels
def filter_image(img):
    if len(img.shape) == 3:
        img_w,img_h,_ = img.shape
    else:
        img_w,img_h = img.shape

    if img_w > 15 and img_h > 15:
        return 1
    else:
        return 0


# Crop out an entire image by each Jigsaw Piece
# Provides Canny Edged output and Normal output
# Also filters out junk pieces
def crop_jigsaw_pieces_from_image(pic, crop_out=False, save=True):
    # load image
    img = cv2.imread(pic)
    rsz_img = cv2.resize(img, None, fx=0.80, fy=0.80) # resize since image is huge
    width, height = rsz_img.shape[:2]

    original = rsz_img.copy()
    gray = cv2.cvtColor(rsz_img, cv2.COLOR_BGR2GRAY)

    # Gaussian vs Median... Median wins for straight edges
    # Blurring with gaussian for better contours
    # blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    blurred = cv2.medianBlur(gray, ksize=3)
    canny = cv2.Canny(blurred, 50, 255, 1)

    kernel = np.ones((3,3), np.uint8)
    dilate = cv2.dilate(canny, kernel, iterations=1)

    cv2.imwrite("CANNY_"+FULL_JIGSAW_IMAGE, dilate)

    # Find contours
    # Tested with [CHAIN_APPROX_SIMPLE, CHAIN_APPROX_NONE, CHAIN_APPROX_TC89_L1, CHAIN_APPROX_TC89_KCOS]
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # Iterate through contours and filter for ROI
    image_number = 0

    img2 = cv2.imread(pic, 0)
    img2 = cv2.resize(img2, None, fx=0.80, fy=0.80) # resize since image is huge

    # https://stackoverflow.com/questions/28759253/how-to-crop-the-internal-area-of-a-contour
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        epsilon = 0.000001 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)

        rsz_img = cv2.drawContours(rsz_img, [approx], 0, (0,255,0), 2)

        if crop_out:
            # Extract out the object and place into JIGSAW_PIECES
            ROI = original[y:y+h, x:x+w]
            if filter_image(ROI):
                crop_shape_dict[NORMAL_JIGSAW_PATH + NORMAL_JIGASW_PIECE.format(image_number)] = ROI
                image_number += 1
            else:
                crop_shape_dict[FILTERED_JUNK_PATH + JUNK_PIECES.format(image_number)] = ROI

    image_number = 0
    if crop_out:
        for i in range(len(cnts)):
            mask = np.zeros_like(img2) # Create mask where white is what we want, black otherwise
            cv2.drawContours(mask, cnts, i, 255, 0) # Draw filled contour in mask

            # Extract out the object and place into CANNY_JIGSAW
            out = np.zeros_like(img2)
            out[mask == 255] = img2[mask == 255]

            # Now crop
            (y, x) = np.where(mask == 255)
            (topy, topx) = (np.min(y), np.min(x))
            (bottomy, bottomx) = (np.max(y), np.max(x))
            out = out[max(0, topy-5): min(width, bottomy+5), max(0, topx-5): min(height, bottomx+5)]

            if filter_image(out):
                crop_shape_dict[CANNY_JIGSAW_PATH + CANNY_JIGASW_PIECE.format(image_number)] = out

                # Extract out the object and place into FULL_IMAGE_CANNY_JIGSAW
                out = np.zeros_like(img2)
                out[mask == 255] = img2[mask == 255]

                # Now crop
                (y, x) = np.where(mask == 0) # Mask == 0 for entire image, 255 for crop
                (topy, topx) = (np.min(y), np.min(x))
                (bottomy, bottomx) = (np.max(y), np.max(x))
                out = out[topy:bottomy+1, topx:bottomx+1]

                crop_shape_dict[FULL_IMAGE_CANNY_JIGSAW_PATH + FULL_IMAGE_CANNY_JIGASW_PIECE.format(image_number)] = out

                image_number += 1

    if save:
        for crop in crop_shape_dict:
            cv2.imwrite(crop, crop_shape_dict[crop])

        logger.info(' %s Successfully split into folders: %s | %s | %s | %s', pic, NORMAL_JIGSAW_PATH,
                    FILTERED_JUNK_PATH, CANNY_JIGSAW_PATH, FULL_IMAGE_CANNY_JIGSAW_PATH)

    cv2.imshow('canny', canny)
    cv2.imshow('image', rsz_img)
    cv2.waitKey(0)


crop_jigsaw_pieces_from_image(FULL_JIGSAW_IMAGE, crop_out=True, save=True)
