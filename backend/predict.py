import numpy as np
import cv2
from backend import image_manipulation as im

def is_empty_square(image):
    edges = cv2.Canny(image, 75, 100)
    contours, hierarchy = im.findContours(edges)
    if len(contours) <= 10: # in case the square has no number, then findContour will return a lot of noise
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            contour_area = w * h
            image_area = image.shape[0] * image.shape[1]
            ratio = contour_area * 100 / image_area 
            if ratio >= 5 and ratio <= 75:
                return False
    return True

def predict_number(small_square, model):

    # this is necessary because an empty square can produce false predictions
    if is_empty_square(small_square):
        return [0]

    target_dimension = 128 # the model was trained with 128x128 images

    # if the input-image is bigger than 128x128,
    # then extract area of interest from the center of the image. 
    if (small_square.shape[0] >= target_dimension) or (small_square.shape[1] >= target_dimension):
        original_dimension = small_square.shape[0]
        buffer = original_dimension - target_dimension
        buffer = 0.15 * buffer

        center_x = small_square.shape[0] // 2
        center_y = small_square.shape[1] // 2

        small_square = small_square[int(center_x - (target_dimension+buffer)//2):int(center_x + (target_dimension+buffer)//2), int(center_y - (target_dimension+buffer)//2):int(center_y + (target_dimension+buffer)//2)]

    # resize image to 128x128
    prediction_data = cv2.resize(small_square, (target_dimension,target_dimension), interpolation=cv2.INTER_AREA)
    prediction_data = prediction_data.reshape(1, target_dimension, target_dimension, 1)

    input_details = model.get_input_details()
    output_details = model.get_output_details()

    input_data = np.array(prediction_data, dtype=np.float32)
    model.set_tensor(input_details[0]['index'], input_data)

    model.invoke()

    prediction = model.get_tensor(output_details[0]['index'])

    prediction = np.argmax(prediction, axis=-1)
    return prediction