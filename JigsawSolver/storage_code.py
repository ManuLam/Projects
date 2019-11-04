# This allows uer input to control the direction of our jigsaw pieces
def test():
    row = 1
    column = 1

    while True:
        print(row, column)

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
        if column > 10 and row < 10:
            column = 1
            row += 1

        if row > 10 and column < 10:
            row = 1
            column += 1

        # Logic for Going up and down, will proceed to next column
        if column < 1 and row > 1:
            column = 10
            row -= 1

        if row < 1 and column < 10:
            row = 10
            column -= 1

        # Logic for Going start and finish, traverse
        if (column < 1 and row == 1) or (row < 1  and column == 1):
            column = 10
            row = 10

        if (column > 10 and row == 10) or (row > 10 and column == 10):
            column = 1
            row = 1

        # Todo Make this logic more generic
        row,column = min(row, 10), min(column, 10)
        row,column = max(1, row), max(1, column)


def piece_finder_with_swirl(path, image, slice_dir):
    row = column = 0
    dx = 0
    dy = -1

    for i in range(max(N_ROWS, N_COLUMNS) ** 2):
        if (-N_ROWS / 2 < row <= N_ROWS / 2) and (-N_COLUMNS / 2 < column <= N_COLUMNS / 2):
            print (row, column)

        try:
            find_piece = '{}{}/slice_{}_{}.png'.format(path, slice_dir, row if row > 9 else '0{}'.format(row),
                                                       column if column > 9 else '0{}'.format(column))

        except:
            print('Cannot find .png file: {}'.format(find_piece))

        try:
            compare_image_main(find_piece, image)
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
            print('Cannot find image {}'.format(find_piece))

        if row == column or (row < 0 and row == -column) or (row > 0 and row == 1 - column):
            dx, dy = -dy, dx
        row, column = row + dx, column + dy


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
