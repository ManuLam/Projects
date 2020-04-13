# RealtimePieceLocator should take an image (Jigsaw Piece) and tries to locate it from camera image (Realtime Image)

import cv2

from JigsawSolver.Legacy_2D_Jigsaw_Solver.PieceLocator import compare_image_main

cap = cv2.VideoCapture(0)
camera = 'camera.jpg'

# Todo
# Real time camera, add a capture every few frames
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

def run():
    while True:
        # Capture frame-by-frames
        ret, frame = cap.read()

        cv2.imwrite(camera, frame)  # save image

        try:
            compare_image_main(camera, 'camera_slice1.jpg')
        except:
            pass


def find_camera():
    for i in range(-1, 1000):
        try:
            cap = cv2.VideoCapture(i)
            print(i + 'True')

        except:
            1

if __name__ == '__main__':
    run()
    #find_camera()

