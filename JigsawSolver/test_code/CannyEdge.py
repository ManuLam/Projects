import cv2
from matplotlib import pyplot as plt


def static(image):
    img = cv2.imread(image,0)
    edges = cv2.Canny(img,100,200)

    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.show()


cap = cv2.VideoCapture(0)
camera = 'dynamic.jpg'


def dynamic():
    while 1:
        # Capture frame-by-frames
        ret, frame = cap.read()

        # Display the resulting frame
        # //cv2.imshow('preview', frame)

        cv2.imwrite(camera, frame)  # save image
        img = cv2.imread(camera, 0)
        edges = cv2.Canny(img, 100, 200)

        '''
        plt.subplot(121),plt.imshow(img,cmap = 'gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(edges,cmap = 'gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

        plt.show(1)
        '''
        cv2.imshow('test', edges)
        cv2.waitKey(1)


original_image = 'jigsaw_image_3.jpg'

#static('jigsaw_image_3.jpg')
dynamic()