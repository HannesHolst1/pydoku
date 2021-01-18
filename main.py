import major_grid as mg
import grid_elements as ge
import cv2

image = cv2.imread('./test_files/test6.jpg')

major_grid = mg.extract_major_grid(image)

ge.extract_grid_elements(major_grid)