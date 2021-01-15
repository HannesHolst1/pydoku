import cv2
import numpy as np
import major_grid as mg

def get_contour_precedence(contour, cols):
    tolerance_factor = 10
    origin = cv2.boundingRect(contour)
    #return ((origin[1] / tolerance_factor) * tolerance_factor) * cols + origin[0]
    return origin[1] + origin[0] / 10

img = mg.search_major_grid('./test_files/test3.jpg')
cv2.imwrite('./debug/test.jpg', img)

# Defining a kernel length
kernel_length = np.array(img).shape[1]//50

# A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
# A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
# A kernel of (3 X 3) ones.
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# Morphological operation to detect vertical lines from an image
img_temp1 = cv2.erode(img, verticle_kernel, iterations=3)
verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
# Morphological operation to detect horizontal lines from an image
img_temp2 = cv2.erode(img, hori_kernel, iterations=3)
horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)

# Weighting parameters, this will decide the quantity of an image to be added to make a new image.
alpha = 0.5
beta = 1.0 - alpha
# This function helps to add two image with specific weight parameter to get a third image as summation of two image.
img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
(thresh, img_final_bin) = cv2.threshold(img_final_bin, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# Find contours for image, which will detect all the boxes
contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contours.sort(key=lambda x:get_contour_precedence(x, img_final_bin.shape[1]))
#contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * img_final_bin.shape[1] )

for i, c in enumerate(contours):
    origin = cv2.boundingRect(c)
    print("x = {}, y = {}: w = {}, h = {}, sort key = {}".format(origin[0], origin[1], origin[2], origin[3], i))

##### debug text
font = cv2.FONT_HERSHEY_SIMPLEX 
org = (50, 50) 
fontScale = 1
color = (0, 255, 0) 
thickness = 2
##### debug text

idy = 0
idx = 1
for i, c in enumerate(contours):
    # Returns the location and width,height for every contour
    x, y, w, h = cv2.boundingRect(c)
    if x > 0 and y > 0 and (w // h < 2):
        idy += 1
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        cv2.drawContours(img_final_bin, [approx], -1, (192,192,192), 3)

        # Using cv2.putText() method str(idx)+'x'+str(idy)
        img_orig = cv2.putText(img_final_bin, str(i), (y+50, x+50), font, fontScale, color, thickness, cv2.LINE_AA) 

        new_img = img[x:x+w, y:y+h] #str(idx)+'x'+str(idy)
        cv2.imwrite('./debug/output/'+ str(i)+ '.png', new_img)
        if idy == 9:
            idx += 1
            idy = 0

print("Total: {}".format(i))
cv2.imwrite('./debug/output/x.png', img_orig)