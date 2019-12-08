import cv2
import numpy as np


def compare_image_main(image_present, image_to_find, color=(255, 0, 255), threshold=.1, show=True):
    return compare_images(image_present, image_to_find, color, threshold, show)


def compare_images(image_present, image_to_find, color, threshold, show):
    img_present, img_to_find = cv2.imread(image_present), cv2.imread(image_to_find)
    result = cv2.matchTemplate(img_to_find, img_present, cv2.TM_SQDIFF_NORMED)

    # We want the minimum squared difference
    mn, _, mnLoc, _ = cv2.minMaxLoc(result)
    loc = np.where(result <= threshold)

    allPts = set()

    if mn <= threshold:
        MPx, MPy = mnLoc  # Extract the coordinates of our best match

        # Step 2: Get the size of the template. This is the same size as the match.
        trows, tcols = img_to_find.shape[:2]
        # Step 3: Draw the rectangle on large_image
        cv2.rectangle(img_present, (MPx, MPy), (MPx + tcols, MPy + trows), (0, 255, 0), 2)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_present, pt, (pt[0] + tcols, pt[1] + trows), color, 1)
        allPts.add((pt[0], pt[1], pt[0] + tcols, pt[1] + trows))

    if show:
        # Display the original image with the rectangle around the match.
        print(image_to_find, mn, threshold)  # print the difference (0-1) to find common threshold
        try:
            find_piece = 'find_piece'
            cv2.namedWindow(find_piece)        # Create a named window
            cv2.moveWindow(find_piece, 0, 0)  # Move it to (40,30)
            cv2.imshow(find_piece, img_present)

            # The image is only displayed if we call this
            cv2.waitKey(1)
        except:
            1

    return MPx, MPy, MPx + tcols, MPy + trows, allPts


cap = cv2.VideoCapture(0)
'''
for i in range(-1, 1000):
    try:
        cap = cv2.VideoCapture(i)
        print(i + 'True')

    except:
        1
'''
camera = 'camera.jpg'


while(True):
    # Capture frame-by-frames
    ret, frame = cap.read()

    # Display the resulting frame
    # //cv2.imshow('preview', frame)

    cv2.imwrite(camera, frame)  # save image

    try:
        compare_image_main(camera, 'camera_slice1.jpg')
    except:
        1

