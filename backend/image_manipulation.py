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

def output_sudoku_solution(image, coordinates, orig_sudoku, solved_sudoku):
    orig_array = np.array(orig_sudoku)
    solved_array = np.array(solved_sudoku)

    output_array = solved_array - orig_array

    font = cv2.FONT_HERSHEY_SIMPLEX 
    fontScale = 3
    color = (255, 0, 0) 
    thickness = 3

    for line_no, line in enumerate(output_array):
        for element_no, element in enumerate(line):
            if element != 0:
                textSize = cv2.getTextSize(str(element), font, fontScale, thickness)
                image = cv2.putText(image, str(element), (coordinates[line_no][element_no][0]+textSize[0][0], coordinates[line_no][element_no][1]+(textSize[0][1]*2)), font, fontScale, color, thickness, cv2.LINE_AA)
    
    return image 