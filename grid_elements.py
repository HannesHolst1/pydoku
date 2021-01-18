import cv2
import numpy as np
import image_manipulation as im
import imutils

def get_contour_precedence(contour):
    origin = cv2.boundingRect(contour)
    return origin[1] /10 + origin[0]

def detect_grid_elements(working_image, contours, hierarchy):
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

    if len(medium_squares) != 9:
        print('Could not determine all medium-sized squares. Analysis cancelled.')
        exit()

    # now, knowing all the medium-sized squares, it is possible to calculate if the area of a square fits roughly 9-10 times into the medium-sized square.
    # medium_squares_properties[i][0] = holds the area of the medium-sized square
    # medium_squares_properties[i][1] = holds the quantity of small-sized squares that belong to the medium-sized square
    small_squares = []
    for contour_index, c in enumerate(contours):
        x, y, w, h = cv2.boundingRect(c)
        candidate = w * h
        for medium_square in medium_squares:
            squares_that_fit = medium_squares_properties[medium_square][0] // candidate
            if (squares_that_fit >= 8) and (squares_that_fit <= 11):
                if medium_squares_properties[medium_square][1] < 9:
                    small_squares.append(contour_index)
                    medium_squares_properties[medium_square][1] += 1
                    break

    if len(small_squares) != 81:
       print('Could not determine all small-sized squares. Analysis cancelled.')
       exit()

    return medium_squares, small_squares

def extract_grid_elements(image):

    img = im.prepare_image(image)

    # # Defining a kernel length
    # kernel_length = np.array(img).shape[1]//50

    # # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    # verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    # # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    # hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # # A kernel of (3 X 3) ones.
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # # Morphological operation to detect vertical lines from an image
    # img_temp1 = cv2.erode(img, verticle_kernel, iterations=3)
    # verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    # # Morphological operation to detect horizontal lines from an image
    # img_temp2 = cv2.erode(img, hori_kernel, iterations=3)
    # horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)

    # # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    # alpha = 0.5
    # beta = 1.0 - alpha
    # # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    # img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = img
    img_final_bin = cv2.Canny(img_final_bin, 75, 200)
    img_final_bin = cv2.erode(~img_final_bin, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    contours, hierarchy  = im.findContours(img_final_bin)

    contours.sort(key=lambda x:get_contour_precedence(x))

    medium_squares, small_squares = detect_grid_elements(img_final_bin, contours, hierarchy)

    # ### debug help
    # for i, c in enumerate(contours):
    #     origin = cv2.boundingRect(c)
    #     print("x = {}, y = {}: w = {}, h = {}, hierarchy[i] = {}, sort key = {}".format(origin[0], origin[1], origin[2], origin[3],hierarchy[0][i], i))

    font = cv2.FONT_HERSHEY_SIMPLEX 
    org = (50, 50) 
    fontScale = 1
    color = (255, 0, 0) 
    thickness = 2
    ##### debug help

    print("medium-sized squares: {}, small-sized squares: {}".format(len(medium_squares), len(small_squares)))

    idy = 0
    idx = 1
    for i, c in enumerate(contours):
        # Returns the location and width,height for every contour
        #if i in medium_squares:
        if i in small_squares:
            x, y, w, h = cv2.boundingRect(c)
            idy += 1
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.015 * peri, True)
            cv2.drawContours(image, [approx], -1, (0,255,0), 1)

            # Using cv2.putText() method 
            img_orig = cv2.putText(image, str(idy)+'x'+str(idx), (x+50, y+50), font, fontScale, color, thickness, cv2.LINE_AA) 

            new_img = img[y:y+h, x:x+w] #str(idx)+'x'+str(idy)
            #cv2.imwrite('./debug/output/'+ str(i)+ '.png', new_img)
            if idy == 9:
                idx += 1
                idy = 0

    if img_orig is None:
        print('Error in processing.')
    else:
        cv2.imwrite('./debug/output/x.png', img_orig)
        