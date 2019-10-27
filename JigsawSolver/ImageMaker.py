import os

from PIL import Image

from JigsawSolver.main import SOLVED_JIGSAW_IMAGE, N_COLUMNS, N_ROWS

width, height = Image.open(SOLVED_JIGSAW_IMAGE).size


i_array = [i for i in range(1, 11)]
j_array = [i for i in range(1, 11)]


image = Image.new('RGB', (int(width/N_COLUMNS), int(height/N_ROWS)), (255, 255, 255))


def create_blank_canvas():
    # Creates an image with blank tiles

    result = Image.new("RGB", (width, height))

    for i in i_array:
        for j in j_array:
            try:
                slice_img = '{}{}/slice_0{}_0{}.png'.format('split_pieces/', 'temp', i, j).replace('010', '10')

                image.save(slice_img, "PNG")

                img = Image.open(slice_img)

                w, h = img.size

                img.thumbnail((w, h), Image.ANTIALIAS)

                x = (j-1) * w
                y = (i-1) * h

                print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
                result.paste(img, (x, y, x + w, y + h))

            except:
                print('bo')
                1

            result.save(os.path.expanduser('image.jpg'))


def create_jigsaw_with_tiles():
    # Creates an image with blank tiles

    result = Image.new("RGB", (width, height))
    slices = [['{}{}/slice_{}_{}.png'.format(path, slice_dir, row if row > 9 else '0{}'.format(row), column if column > 9 else '0{}'.format(column))
               for row in range(1, N_ROWS+1)] for column in range(1, N_COLUMNS+1)]

    for i in i_array:
        for j in j_array:
            try:
                slice_img = '{}{}/slice_0{}_0{}.png'.format('split_pieces/', 'temp', i, j).replace('010', '10')

                img = Image.open(slice_img)

                w, h = img.size

                img.thumbnail((w, h), Image.ANTIALIAS)

                x = (j-1) * w
                y = (i-1) * h

                print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
                result.paste(img, (x, y, x + w, y + h))

            except:
                print('Couldnt create jigsaw with tiles')

            result.save(os.path.expanduser('image.jpg'))


result = Image.new("RGB", (width, height))


def put_piece_in_jigsaw(index_i, index_j, slice_img, canvas_name):
    # Places a single piece into a Blank Jigsaw template

    img = Image.open(slice_img)

    w, h = img.size

    img.thumbnail((w, h), Image.ANTIALIAS)

    x = (index_j-1) * w
    y = (index_i-1) * h

    print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
    result.paste(img, (x, y, x + w, y + h))

    result.save(os.path.expanduser(canvas_name))
