import cv2

import numpy as np
from PIL import Image

#from getkey import getkey, keys

from JigsawSolver.ImageMaker import put_piece_in_jigsaw
from JigsawSolver.main import SOLVED_JIGSAW_IMAGE, N_COLUMNS, N_ROWS


def compare_image_main(image_to_find, main_image, diff=.005, show=True):
    return compare_images_jigsaw(main_image, image_to_find, diff, show)


def compare_images_jigsaw(image_present, image_to_find, diff, show):
    img_scrabbled_jigsaw, img_to_find = cv2.imread(image_present), cv2.imread(image_to_find)
    img_initial_jigsaw_image = cv2.imread(SOLVED_JIGSAW_IMAGE)

    result_in_jigsaw = cv2.matchTemplate(img_to_find, img_scrabbled_jigsaw, cv2.TM_SQDIFF_NORMED)
    result_in_initial_jigsaw_image = cv2.matchTemplate(img_to_find, img_initial_jigsaw_image, cv2.TM_SQDIFF_NORMED)

    # We want the minimum squared difference
    mn, _, mnLoc, _ = cv2.minMaxLoc(result_in_jigsaw)
    mn2, _, mnLoc2, _ = cv2.minMaxLoc(result_in_initial_jigsaw_image)
    loc = np.where(result_in_jigsaw <= diff)

    allPts = set()

    if mn <= diff:
        # Draw the rectangle:
        # Extract the coordinates of our best match

        MPx, MPy = mnLoc

        # Step 2: Get the size of the template. This is the same size as the match.
        trows, tcols = img_to_find.shape[:2]
        # Step 3: Draw the rectangle on large_image
        cv2.rectangle(img_scrabbled_jigsaw, (MPx, MPy), (MPx + tcols, MPy + trows), (0, 255, 0), 2)

    if mn2 <= diff:
        # Draw the rectangle:
        # Extract the coordinates of our best match

        MPx2, MPy2 = mnLoc2

        # Step 2: Get the size of the template. This is the same size as the match.
        trows2, tcols2 = img_to_find.shape[:2]
        # Step 3: Draw the rectangle on large_image
        cv2.rectangle(img_initial_jigsaw_image, (MPx2, MPy2), (MPx2 + tcols2, MPy2 + trows2), (0, 255, 0), 2)

    '''Algorithm for placing all possible locations for scrabbled jigsaw'''
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_scrabbled_jigsaw, pt, (pt[0] + tcols, pt[1] + trows), (255, 0, 255), 2)
        allPts.add((pt[0], pt[1], pt[0] + tcols, pt[1] + trows))

    if show:
        # Display the original image with the rectangle around the match.
        print(image_to_find, mn, diff, 'Total amount of matches: {}'.format(
            sum(1 for _ in zip(*loc[::-1]))))  # print the difference (0-1) to find common diff

        width, height = Image.open(image_present).size

        solved_jigsaw_image = 'ORGINAL_IMAGE'
        cv2.namedWindow(solved_jigsaw_image)  # Create a named window
        cv2.moveWindow(solved_jigsaw_image, 0, 0)  # Move it to (40,30)
        cv2.imshow(solved_jigsaw_image, img_initial_jigsaw_image)

        jigsaw_img = 'JIGSAW_IMAGE'
        cv2.namedWindow(jigsaw_img)  # Create a named window
        cv2.moveWindow(jigsaw_img, 0, height + 62)  # Move it to (40,30)
        cv2.imshow(jigsaw_img, img_scrabbled_jigsaw)

        find_piece = 'find_piece'
        cv2.namedWindow(find_piece)  # Create a named window
        cv2.moveWindow(find_piece, 0, (height + 70) * 2)  # Move it to (40,30) #(width+20)*2
        cv2.imshow(find_piece, img_to_find)

        # The image is only displayed if we call this
        cv2.waitKey(50)

    return MPx, MPy, MPx + tcols, MPy + trows, allPts


i_array = [i for i in range(1, 11)]
j_array = [i for i in range(1, 11)]


# Automatic
def piece_finder(path, image, slice_dir):
    for i in i_array:
        for j in j_array:
            try:
                find_piece = '{}{}/slice_0{}_0{}.png'.format(path, slice_dir, i, j).replace('010', '10')

            except:
                print('Cannot find .png file: {}'.format(find_piece))

            try:
                compare_image_main(find_piece, image)

                canvas_name = 'blank_jigsaw_board.jpg'

                # Kinda Naive solution in placing jigsaws into board
                put_piece_in_jigsaw(i, j, find_piece, canvas_name)

                blank_jigsaw_board = 'BLANK_BOARD'
                cv2.namedWindow(blank_jigsaw_board)  # Create a named window
                cv2.moveWindow(blank_jigsaw_board, 2000, 0)  # Move it to (40,30)

                cv2_canvas_name = cv2.imread(filename=canvas_name)
                cv2.imshow(blank_jigsaw_board, cv2_canvas_name)
                cv2.waitKey(1)

            except:
                print('Cannot find image {}'.format(find_piece))
                raise

'''
# Manual
def piece_finder_with_buttons(path, image, slice_dir, diff=0.2):
    row = 1
    column = 1

    while True:
        cant_find = False

        print(row, column)

        try:
            find_piece = '{}{}/slice_{}_{}.png'.format(path, slice_dir, row if row > 9 else '0{}'.format(row),
                                                       column if column > 9 else '0{}'.format(column))

        except:
            print('Cannot find .png file: {}'.format(find_piece))

        try:
            compare_image_main(find_piece, image, diff)
            canvas_name = 'blank_jigsaw_board.jpg'

            # Kinda Naive solution in placing jigsaws into board
            put_piece_in_jigsaw(row, column, find_piece, canvas_name)

            blank_jigsaw_board = 'BLANK_BOARD'
            cv2.namedWindow(blank_jigsaw_board)  # Create a named window
            cv2.moveWindow(blank_jigsaw_board, 350, 0)  # Move it to (40,30)

            cv2_canvas_name = cv2.imread(filename=canvas_name)
            cv2.imshow(blank_jigsaw_board, cv2_canvas_name)
            cv2.waitKey(1)

        except:
            cant_find = True
            print('Cannot find image {}'.format(find_piece))

        key = getkey()

        if key == keys.LEFT:
            column -= 1

        elif key == keys.RIGHT:
            column += 1

        elif key == keys.UP:
            row -= 1

        elif key == keys.DOWN:
            row += 1

        # Logic for Going left and right, will proceed to next row
        if column > N_COLUMNS and row < N_ROWS:
            column = 1
            row += 1

        if row > N_ROWS and column < N_COLUMNS:
            row = 1
            column += 1

        # Logic for Going up and down, will proceed to next column
        if column < 1 and row > 1:
            column = N_COLUMNS
            row -= 1

        if row < 1 and (column < N_COLUMNS and column != 1):
            row = N_ROWS
            column -= 1

        # Logic for Going start and finish, traverse
        if (column < 1 and row == 1) or (row < 1 and column == 1):
            column = N_COLUMNS
            row = N_ROWS

        if (column > N_COLUMNS and row == N_ROWS) or (row > N_ROWS and column == N_COLUMNS):
            column = 1
            row = 1

        # Todo Make this logic more generic
        row, column = min(row, N_ROWS), min(column, N_COLUMNS)
        row, column = max(1, row), max(1, column)
'''

def piece_finder_with_swirl(path, image, slice_dir, diff=0.2):
    slices = [['{}{}/slice_{}_{}.png'.format(path, slice_dir, row if row > 9 else '0{}'.format(row), column if column > 9 else '0{}'.format(column))
               for row in range(1, N_ROWS+1)] for column in range(1, N_COLUMNS+1)]

    spiral_slices = return_spiral_matrix(slices)

    for img_slice_full_path in spiral_slices:
        # slice looks like '{}{}/slice_{}_{}.png'

        image_name = img_slice_full_path.split('/')[-1][:-4]

        print(image_name)

        strip_numbers = [int(s) for s in image_name.split('_') if s.isdigit()]

        print(strip_numbers)

        row,column = strip_numbers[0], strip_numbers[1]

        try:
            compare_image_main(img_slice_full_path, image, diff=diff)
            canvas_name = 'blank_jigsaw_board.jpg'

            # Placing jigsaws pieces into board with a spiral pattern
            put_piece_in_jigsaw(row, column, img_slice_full_path, canvas_name)

            blank_jigsaw_board = 'BLANK_BOARD'
            cv2.namedWindow(blank_jigsaw_board)  # Create a named window
            cv2.moveWindow(blank_jigsaw_board, 350, 0)  # Move it to (40,30)

            cv2_canvas_name = cv2.imread(filename=canvas_name)
            cv2.imshow(blank_jigsaw_board, cv2_canvas_name)
            cv2.waitKey(1)

        except:
            print('Cannot find image {}'.format(img_slice_full_path))
            raise


def return_spiral_matrix(dimensional_list):
    spiral_slices = []

    while dimensional_list:
        for x in dimensional_list.pop(0):
            spiral_slices.append(x)

        for v in dimensional_list:
            spiral_slices.append(v.pop())

        if dimensional_list:
            for x in dimensional_list.pop()[::-1]:
                spiral_slices.append(x)

        for v in dimensional_list[::-1]:
            spiral_slices.append(v.pop(0))

    return spiral_slices
