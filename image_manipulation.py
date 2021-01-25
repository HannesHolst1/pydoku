import cv2
import numpy as np

def prepare_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    image = cv2.GaussianBlur(image, (5,5), 0)

    (thresh, image) = cv2.threshold(image, 128, 255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)

    image = 255-image

    return image

def identify_edges(image):
    return cv2.Canny(image, 75, 100)

def findContours(image):
    return cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

def output_sudoku_solution(image, orig_sudoku, solved_sudoku):
    orig_array = np.array(orig_sudoku)
    solved_array = np.array(solved_sudoku)

    output_array = solved_array - orig_array

    font = cv2.FONT_HERSHEY_SIMPLEX 
    fontScale = 3
    color = (255, 0, 0) 
    thickness = 3

    x_steps = int(image.shape[0] // 9)
    y_steps = int(image.shape[1] // 9)

    x_pos = 0
    y_pos = y_steps

    for line in output_array:
        for element in line:
            x_pos += x_steps
            if x_pos > image.shape[0]:
                x_pos = x_steps
                y_pos += y_steps

            if element != 0:
                image = cv2.putText(image, str(element), (x_pos - int(x_steps-x_steps//3), y_pos - int(y_steps//4)), font, fontScale, color, thickness, cv2.LINE_AA)
    
    return image 