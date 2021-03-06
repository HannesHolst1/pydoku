import numpy as np
import imutils
import cv2
from backend import image_manipulation as im

def order_points(pts):
	rect = np.zeros((4, 2), dtype = "float32")

	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]

	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]

	return rect

def four_point_transform(image, pts):
	rect = order_points(pts)
	(tl, tr, br, bl) = rect

	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))

	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))

	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	
	return warped

def find_grid_by_edges(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    img = cv2.GaussianBlur(img, (5,5), 0)

    img = cv2.threshold(img, 128, 255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]

    img = 255-img

    img_edged = im.identify_edges(img)

    cnts = im.findContours(img_edged)

    ## if possible replace below by internal algorithm
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

    # loop over our contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.06 * peri, True)

        dimensions = cv2.boundingRect(c)

        if (len(approx) == 4):
            dimensions = cv2.boundingRect(c)
            cropped = four_point_transform(image, approx.reshape(4, 2))
            return cropped, dimensions

    return None, None

def find_grid_by_contentarea(image, minium_ratio=0.15):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    img = cv2.GaussianBlur(img, (5,5), 0)

    img = cv2.threshold(img, 128, 255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]

    img = 255-img

    kernel = np.ones((5,5),np.uint8)
    img = cv2.dilate(img, kernel, iterations=4)

    cnts = im.findContours(img)

    ## if possible replace below by internal algorithm
    cnts = imutils.grab_contours(cnts)

    # loop over our contours
    image_area = image.shape[0] * image.shape[1]
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.06 * peri, True)

        dimensions = cv2.boundingRect(c)

        current_Rect_area = dimensions[2] * dimensions[3]
        if (current_Rect_area / image_area >= minium_ratio) and (len(approx) == 4):
            cropped = four_point_transform(image, approx.reshape(4, 2))
            return cropped, dimensions

    return None, None	