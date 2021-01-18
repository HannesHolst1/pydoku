import major_grid as mg
import grid_elements as ge
import cv2

print("test1 (should work):")
image = cv2.imread('./test_files/test1.jpg')
major_grid = mg.extract_major_grid(image)
ge.extract_grid_elements(major_grid)

print("-----------------------")
print("test2 (should work):")
image = cv2.imread('./test_files/test2.jpg')
major_grid = mg.extract_major_grid(image)
ge.extract_grid_elements(major_grid)

print("-----------------------")
print("test3 (should work):")
image = cv2.imread('./test_files/test3.jpg')
major_grid = mg.extract_major_grid(image)
ge.extract_grid_elements(major_grid)

print("-----------------------")
print("test4 (fail is ok):")
image = cv2.imread('./test_files/test4.jpg')
major_grid = mg.extract_major_grid(image)
ge.extract_grid_elements(major_grid)

print("-----------------------")
print("test5 (should work):")
image = cv2.imread('./test_files/test5.jpg')
major_grid = mg.extract_major_grid(image)
ge.extract_grid_elements(major_grid)

print("-----------------------")
print("test6 (???):")
image = cv2.imread('./test_files/test6.jpg')
major_grid = mg.extract_major_grid(image)
ge.extract_grid_elements(major_grid)

print("-----------------------")
print("test7 (???):")
image = cv2.imread('./test_files/test7.jpg')
major_grid = mg.extract_major_grid(image)
ge.extract_grid_elements(major_grid)

print("-----------------------")
print("test8 (???):")
image = cv2.imread('./test_files/test8.jpg')
major_grid = mg.extract_major_grid(image)
ge.extract_grid_elements(major_grid)

print("-----------------------")
print("test9 (???):")
image = cv2.imread('./test_files/test9.jpg')
major_grid = mg.extract_major_grid(image)
ge.extract_grid_elements(major_grid)

print("-----------------------")
print("test10 (???):")
image = cv2.imread('./test_files/test10.jpg')
major_grid = mg.extract_major_grid(image)
ge.extract_grid_elements(major_grid)

print("-----------------------")
print("test11 (???):")
image = cv2.imread('./test_files/test11.jpg')
major_grid = mg.extract_major_grid(image)
ge.extract_grid_elements(major_grid)

print("-----------------------")
print("test12 (should work):")
image = cv2.imread('./test_files/test12.jpg')
major_grid = mg.extract_major_grid(image)
ge.extract_grid_elements(major_grid)

print("-----------------------")
print("test13 (should work):")
image = cv2.imread('./test_files/test13.jpg')
major_grid = mg.extract_major_grid(image)
ge.extract_grid_elements(major_grid)
