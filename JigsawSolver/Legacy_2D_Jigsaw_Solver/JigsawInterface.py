# Image splitter, takes an image and splits it into a dir
# Image joiner, stakes the splits and creates a randomized jigsaw

from PyQt5.QtWidgets import QApplication

from JigsawSolver.ImageSplitter import image_splitter
from JigsawSolver.PieceLocator import piece_finder, compare_image_main, \
    piece_finder_with_swirl
from JigsawSolver.ImagePieceJoiner import piece_joiner
from JigsawSolver.main import N_PIECES, PATH, SLICE_DIR, UNSOLVED_JIGSAW_IMAGE, SOLVED_JIGSAW_IMAGE
from SetupEnvironment import setup


def create_jigsaw_from_image(solved_jigsaw_image, unsolved_jigsaw_image, number_of_pieces=N_PIECES):
    tiles = image_splitter(solved_jigsaw_image, unsolved_jigsaw_image, number_of_pieces, save=True)
    piece_joiner(tiles, number_of_pieces, unsolved_jigsaw_image, scramble_jigsaw=True)


class Button:
    root = Tk()
    root.title("Interface!")
    root.geometry("1000x150+50+50")

    # Create a button that will print the contents of the entry
    create = Button(root, text='Create new Jigsaw', command='fish')
    spiral = Button(root, text='Solve with Spiral', command='piece_finder_with_swirl(PATH, UNSOLVED_JIGSAW_IMAGE, SLICE_DIR, diff=0.005)')
    arrows = Button(root, text='Solve with Arrows', command='stop')

    create.grid()
    spiral.grid()
    arrows.grid()

    #root.mainloop()

# Create a GUI with options
if __name__ == '__main__':
    # Setting up Environment
    setup()

    app = QApplication([])
    button = Button()
    button.show()

    # Linking buttons into our interface
    create_jigsaw_from_image(SOLVED_JIGSAW_IMAGE, UNSOLVED_JIGSAW_IMAGE, N_PIECES)
    # blank_canvas()

    #piece_finder_with_buttons(PATH, UNSOLVED_JIGSAW_IMAGE, SLICE_DIR, diff=0.005)
    piece_finder_with_swirl(PATH, UNSOLVED_JIGSAW_IMAGE, SLICE_DIR, diff=0.005)

