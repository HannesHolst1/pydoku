from typing import get_origin
import numpy as np
import cv2
import image_manipulation as im

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

    target_dimension = 128

    if (small_square.shape[0] >= target_dimension) or (small_square.shape[1] >= target_dimension):
        original_dimension = small_square.shape[0]
        buffer = original_dimension - target_dimension
        buffer = 0.15 * buffer

        center_x = small_square.shape[0] // 2
        center_y = small_square.shape[1] // 2

        small_square = small_square[int(center_x - (target_dimension+buffer)//2):int(center_x + (target_dimension+buffer)//2), int(center_y - (target_dimension+buffer)//2):int(center_y + (target_dimension+buffer)//2)]

    prediction_data = cv2.resize(small_square, (target_dimension,target_dimension), interpolation=cv2.INTER_AREA)
    prediction_data = prediction_data.reshape(1, target_dimension, target_dimension, 1)

    prediction = np.argmax(model.predict(prediction_data), axis=-1)
    return prediction