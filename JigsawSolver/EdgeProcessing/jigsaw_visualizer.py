import cv2
from PIL import Image


# Specific location has location in our template
def template_maker(N, width, height, pieces, save=None, show=False):
    background = Image.new('RGB', (N*width, N*height), 'black')
    background.save(save)
    piece_locations = []

    for i in range(len(pieces)):
        for j in range(len(pieces[i])):
            img = Image.open(pieces[i][j])

            background.paste(img, (width*j, height*i))
            background.save(save)

    if show:
        background.show()

    return piece_locations


# Swap two pieces inside a 2D list, pieces=Jigsaw object
# Make a new image of a "swapped list"
def template_piece_swapper(N, width, height, pieces, save=None, piece1=None, piece2=None, show=False):
    # extract piece1, piece2 and swap them
    # pieces = new pieces
    print(piece1, piece2)
    p11,p12 = 0,0
    p21,p22 = 0,0

    for index in range(len(pieces)):

        try:
            if pieces[index].index(piece1):
                p11 = index
                p12 = pieces[index].index(piece1)

                print("p1 found: ", pieces[index])

        except ValueError:
            pass

        try:
            if pieces[index].index(piece2):
                p21 = index
                p22 = pieces[index].index(piece2)
                print("p2 found: ", pieces[index])

        except ValueError:
            pass

    pieces[p11][p12], pieces[p21][p22] = piece2, piece1

    template_maker(N, width, height, pieces, save=save, show=show)


# Find largest width and height of extracted pieces
def find_max_edge_size(pieces):
    w, h = 0,0

    for image in pieces:
        image_w, image_h = cv2.imread(image).shape[:2]
        h = max(h, image_h)
        w = max(w, image_w)

    return h,w


# merges all progress stages into one png image
def progress_merger():
    1

# Enhances customer experience from knowing which piece is which during solving steps
def piece_labeler():
    1

# Returns a N*N sized list
def n_piece_splitter(N, pieces):
    return [pieces[i:i + N-1] for i in range(0, len(pieces), N-1)]
