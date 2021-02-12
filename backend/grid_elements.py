import cv2
import numpy as np
from backend import image_manipulation as im

def get_contour_precedence(contour):
    origin = cv2.boundingRect(contour)
    return origin[1] + origin[0] / 10

def detect_grid_elements(working_image, contours):
    # the function "extract_major_grid" made sure, that we have the Sudoku extracted from the rest of the picture.
    # that means, the width and height of the working image represents roughly the width and height of the Sudoku itself. 
    sudoku_area = working_image.shape[0] * working_image.shape[1]

    # the findContours function will find three sizes of squares: 
    # the Sudoku itself, medium sized squares that contain small squares, and small squares which do contain the numbers.
    # now, knowing the area of the Sudoku, it is possible to determine the medium sized squares-
    medium_squares = []
    medium_squares_properties = {}
    for contour_index, c in enumerate(contours):
       x, y, w, h = cv2.boundingRect(c)
       candidate = w * h
       # the area of the candidate must fit appr. 9 times into the Sudoku.
       # Only 9x9 Sudokus are supported with this solution (most Sudokus in newspapers are 9x9)
       squares_that_fit = sudoku_area // candidate
       if (squares_that_fit == 9):
           medium_squares.append(contour_index)
           medium_squares_properties[contour_index] = [candidate, 0]         

    # now, knowing all the medium-sized squares, it is possible to calculate if the area of a small square fits roughly 8-11 times into the medium-sized square.
    # medium_squares_properties[i][0] = holds the area of the medium-sized square
    # medium_squares_properties[i][1] = holds the quantity of small-sized squares that belong to the medium-sized square
    small_squares = []
    ignore_coordinates = []
    for contour_index, c in enumerate(contours):
        x, y, w, h = cv2.boundingRect(c)
        # when a square is valid, the coordinates of the top left corner and bottom right corner are stored.
        # all contours within these coordinates are ignored and not processed. 
        ignore_contour = [(x >= ignore_coordinate[0] and x <= ignore_coordinate[2]) and (y >= ignore_coordinate[1] and y <= ignore_coordinate[3]) for ignore_coordinate in ignore_coordinates]
        if not any(ignore_contour):
            candidate = w * h
            for medium_square in medium_squares:
                squares_that_fit = medium_squares_properties[medium_square][0] // candidate
                if (squares_that_fit >= 8) and (squares_that_fit <= 11):
                    if medium_squares_properties[medium_square][1] < 9:
                        small_squares.append(contour_index)
                        medium_squares_properties[medium_square][1] += 1
                        ignore_coordinates.append([x, y, x+w, y+h])
                        break

    return medium_squares, small_squares

def get_squares_with_canny(image):
    image = cv2.Canny(image, 75, 200)
    image = cv2.erode(~image, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
    (thresh, image) = cv2.threshold(image, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    contours, hierarchy  = im.findContours(image)
    contours.sort(key=lambda x:get_contour_precedence(x))
 
    medium_squares, small_squares = detect_grid_elements(image, contours)
    sudoku_recognized = (len(medium_squares) == 9) and (len(small_squares) == 81)

    return sudoku_recognized, small_squares, contours

def get_squares_with_xlines(img):
    # Defining a kernel length
    kernel_length = np.array(img).shape[1]//60

    if kernel_length == 0:
        return False, None, None

    # A vertical kernel of (1 X kernel_length), which will detect all the vertical lines from the image.
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Morphological operation to detect vertical lines from an image
    img_temp1 = cv2.erode(img, vertical_kernel, iterations=3)
    vertical_lines_img = cv2.dilate(img_temp1, vertical_kernel, iterations=3)
    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)

    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(vertical_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    contours, hierarchy  = im.findContours(img_final_bin)

    contours.sort(key=lambda x:get_contour_precedence(x))

    # validate grid
    sudoku_area = img_final_bin.shape[0] * img_final_bin.shape[1]

    small_squares = []
    for contour_index, c in enumerate(contours):
       x, y, w, h = cv2.boundingRect(c)     
       candidate = w * h
       squares_that_fit = sudoku_area // candidate
       if (squares_that_fit >= 75) and (squares_that_fit <= 105):
           if len(small_squares) < 81:
                small_squares.append(contour_index)

    sudoku_recognized = (len(small_squares) == 81)

    return sudoku_recognized, small_squares, contours

def extract_grid_elements(image, name='output'):

    img = im.prepare_image(image)

    grid_identified, squares, contours = get_squares_with_canny(img)

    if grid_identified:
        print('using Canny, squares: {}'.format(len(squares)))
    else:
        print('Canny failed.')

    if not grid_identified:
        grid_identified, squares, contours = get_squares_with_xlines(img)
        if grid_identified:
            print('using xlines, squares: {}'.format(len(squares)))
        else:
            print('xlines failed.')

    if not grid_identified:
        if squares is None:
            return None, None

    idy = 0
    idx = 1
    numbers = []
    grid_columns = []
    coordiantes_line = []
    coordinates = []
    for i, c in enumerate(contours):
        if i in squares:
            x, y, w, h = cv2.boundingRect(c)
            idy += 1
            coordiantes_line.append([x, y, w, h])
            new_img = image[y:y+h, x:x+w]
            grid_columns.append(new_img)
            if idy == 9:
                idy = 0
                numbers.insert(idx, grid_columns)
                coordinates.insert(idx, coordiantes_line)
                idx += 1
                grid_columns = []
                coordiantes_line = []

    return numbers, coordinates
        