import logging

import cv2
import numpy as np

from global_config import ORIGINAL_JIGSAW_PATH, ORIGINAL_JIGASW_PIECE, \
    CANNY_JIGSAW_PATH, CANNY_JIGASW_PIECE, FULL_IMAGE_CANNY_JIGSAW_PATH, \
    FULL_IMAGE_CANNY_JIGASW_PIECE, JUNK_PIECES, FILTERED_JUNK_PATH

crop_rect_dict = {}
crop_shape_dict = {}

logger = logging.getLogger(__name__)


def filter_out_image(img):
    """
    This function counts the total amount of pixels (15 in our case) within an image
    Mainly used for filtering noise disturbances

    :param img: Image to be checked
    :return: 1 implies Image is smaller than 15 pixels, 0 implies Image is larger than 15 pixels
    """
    if len(img.shape) == 3:
        img_w,img_h,_ = img.shape
    else:
        img_w,img_h = img.shape

    if img_w > 15 and img_h > 15:   # If there are more than 15 pixels, return 0
        return 0
    else:                           # If there are less than 15 pixels, return 1
        return 1


def crop_jigsaw_pieces_from_image(image_to_extract, crop_out=False, show=False, save=True):
    """
    This function extracts all Jigsaw pieces from an image
    It provides the Original Jigsaw pieces and a Canny Edge version of the Jigsaw pieces
    It also filters out all extracted images that are below 15 pixels (noise disturbances)

    :param image_to_extract: This is the image we want to extract the Jigsaw pieces from
    :param crop_out: A boolean that allows us to crop out pieces if wanted
    :param show: A boolean that allows us to see the progress of this function if wanted
    :param save: A boolean that allows us to save our extracted Jigsaw pieces if wanted
    """

    img = cv2.imread(image_to_extract)  # read in image input
    rsz_img = cv2.resize(img, None, fx=0.80, fy=0.80)  # resize our image, since it is huge
    width, height = rsz_img.shape[:2]   # Extract the width and height of this resized image

    original = rsz_img.copy()   # Copy this resized image for later use
    gray = cv2.cvtColor(rsz_img, cv2.COLOR_BGR2GRAY)    # Turn the resized image to greyscale, for Canny Edge use

    # Tried Gaussian Filter and Median Filter, The Median Filter is better for preserving straight edges
    blurred = cv2.medianBlur(gray, ksize=3)  # Setup the blue to be applied later
    canny = cv2.Canny(blurred, 50, 255, 1)  # Blurs the gray-scaled image, to improve edge detection

    kernel = np.ones((3,3), np.uint8)   # A kernel that returns a larger result for dilation
    dilate = cv2.dilate(canny, kernel, iterations=1)  # Dilating our Jigsaw piece image to allow for easier debugging

    # Create an image that can later be used for debugging junk pieces
    cv2.imwrite("debug_junk_pieces.png", dilate)

    # Find contours
    # Tested with [CHAIN_APPROX_SIMPLE, CHAIN_APPROX_NONE, CHAIN_APPROX_TC89_L1, CHAIN_APPROX_TC89_KCOS]
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]   # Extract the contours at the location according to size of list

    # Iterate through contours and filter for ROI
    image_number = 0

    img2 = cv2.imread(image_to_extract, 0)  # read in image input
    img2 = cv2.resize(img2, None, fx=0.80, fy=0.80)  # resize our image, since it is huge

    # Loop through all the contours that were found earlier
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)   # Returns the best rectangle fit for our Jigsaw piece

        epsilon = 0.000001 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)

        rsz_img = cv2.drawContours(rsz_img, [approx], 0, (0, 255, 0), 2)  # Draw the contours back on or Original Image

        if crop_out:
            # Extract out the Jigsaw piece and place into JIGSAW_PIECES
            ROI = original[y:y+h, x:x+w]

            # Filters the Junk pieces into a separate DIR
            if not filter_out_image(ROI):
                crop_shape_dict[ORIGINAL_JIGSAW_PATH + ORIGINAL_JIGASW_PIECE.format(image_number)] = ROI  # Add to dict
                image_number += 1
            else:
                crop_shape_dict[FILTERED_JUNK_PATH + JUNK_PIECES.format(image_number)] = ROI

    image_number = 0
    if crop_out:
        for i in range(len(cnts)):
            mask = np.zeros_like(img2)  # Create a mask where white is what we want, black otherwise
            cv2.drawContours(mask, cnts, i, 255, 0)  # Draw filled contour in mask

            # Extract out the Canny Jigsaw piece and place into CANNY_JIGSAW
            out = np.zeros_like(img2)
            out[mask == 255] = img2[mask == 255]    # Mask out white pixels

            # Now crop out the mask
            (y, x) = np.where(mask == 255)  # Extract all the y and x pixels from the mask
            (topy, topx) = (np.min(y), np.min(x))  # Return the min of all the y and x
            (bottomy, bottomx) = (np.max(y), np.max(x))  # Return the max of all the y and x

            # Output image for Canny Image
            out = out[max(0, topy-5): min(width, bottomy+5), max(0, topx-5): min(height, bottomx+5)]

            if not filter_out_image(out):   # If we don't need to filter this image piece
                crop_shape_dict[CANNY_JIGSAW_PATH + CANNY_JIGASW_PIECE.format(image_number)] = out  # Add to dict

                # Extract out the object and place into FULL_IMAGE_CANNY_JIGSAW
                out = np.zeros_like(img2)
                out[mask == 255] = img2[mask == 255]

                # Now crop
                (y, x) = np.where(mask == 0) # Mask == 0 for entire image, 255 for crop
                (topy, topx) = (np.min(y), np.min(x))  # Return the min of all the y and x
                (bottomy, bottomx) = (np.max(y), np.max(x))  # Return the max of all the y and x
                out = out[topy:bottomy+1, topx:bottomx+1]  # Output image for Full Canny Image

                # Add to dict
                crop_shape_dict[FULL_IMAGE_CANNY_JIGSAW_PATH + FULL_IMAGE_CANNY_JIGASW_PIECE.format(image_number)] = out

                image_number += 1

    # If we want to save the outputs, it goes through our dictionary and saves all the images to their exact DIR
    if save:
        for crop in crop_shape_dict:
            cv2.imwrite(crop, crop_shape_dict[crop])    # Write the image file

        logger.info(' %s Successfully split into folders: %s | %s | %s | %s', image_to_extract, ORIGINAL_JIGSAW_PATH,
                    FILTERED_JUNK_PATH, CANNY_JIGSAW_PATH, FULL_IMAGE_CANNY_JIGSAW_PATH)    # Logging

    cv2.imshow('CannyEdgeImage', canny)
    cv2.imshow('OriginalImage', rsz_img)
    cv2.waitKey(0)
