import numpy as np
import cv2
import image_manipulation as im
from skimage.feature import hog

def is_empty_square(image):
    edges = cv2.Canny(image, 75, 100)
    contours, hierarchy = im.findContours(edges)
    if len(contours) <= 10: # in case the square has no number, then findContour will return a lot of noise
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            contour_area = w * h
            image_area = image.shape[0] * image.shape[1]
            ratio = contour_area * 100 / image_area 
            if ratio >= 5 and ratio <= 25:
                return False
    return True

def predict_number(small_square, model):

    if is_empty_square(small_square):
        return [0]

    if small_square.shape[0] < small_square.shape[1]:
        small_square = small_square[0+30:small_square.shape[0]-30, 0+30:small_square.shape[0]-30]
    else:
        small_square = small_square[0+30:small_square.shape[1]-30, 0+30:small_square.shape[1]-30]

    new_img = cv2.resize(small_square, (128,128), interpolation=cv2.INTER_AREA)
    prediction_data = hog(new_img, orientations=8, pixels_per_cell=(10,10), cells_per_block=(5, 5))      

    prediction_data = prediction_data.reshape(1, -1)

    prediction = model.predict(prediction_data)
    return prediction