from cvzone.SelfiSegmentationModule import SelfiSegmentation 
import numpy as np
import cv2

cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW) # Windows
segmenter = SelfiSegmentation(1)

WIDTH, HEIGHT = 1920, 1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

cell_width, cell_height = 10, 15
new_width, new_height = int(WIDTH / cell_width), int(HEIGHT / cell_height)
new_dimensions = (new_width, new_height)

chars = " .,-~:;=!*#$@"
norm = 255 / len(chars)
font = cv2.FONT_HERSHEY_SIMPLEX
font_size = 0.4

def matrix(image):
    global matrix_win

    matrix_win = np.zeros(
        (HEIGHT, WIDTH, 3), 
        np.uint8
    )

    small_img = cv2.resize(
        image, 
        new_dimensions, 
        interpolation=cv2.INTER_NEAREST
    )
    small_img = segmenter.removeBG(small_img, (0, 0, 0))
    gray_img = cv2.cvtColor(
        small_img, 
        cv2.COLOR_BGR2GRAY
    )

    for i in range(new_height):
        for j in range(new_width):
            intensity = gray_img[i, j]
            char_index = int(intensity / norm)
            color = small_img[i, j]
            B = int(color[0])
            G = int(color[1])
            R = int(color[2])

            char = chars[char_index]
            cv2.putText(
                matrix_win, 
                char, 
                (
                    j * cell_width + 5, 
                    i * cell_height + 12
                ), 
                font, 
                font_size, 
                (B, G, R), 
                1
            )

def video(frames, filename):
    if not cap.isOpened():
        raise IOError("Can't open webcam")

    filename = str(filename) + ".mp4"

    fourcc = cv2.VideoWriter_fourcc('H','2','6','4')
    out = cv2.VideoWriter(filename, fourcc, frames, (WIDTH, HEIGHT))

    while True:
        _, frame = cap.read()
        result = frame.copy()

        matrix(result)

        out.write(matrix_win)
        
        #cv2.imshow('ASCII Webcam', matrix_win)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def photo(filename):
    filename = str(filename) + ".png"

    _, frame = cap.read()
    result = frame.copy()

    matrix(result)
    cv2.imwrite(filename, matrix_win)