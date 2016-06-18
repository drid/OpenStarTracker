import numpy as np
import cv2


# Load an example image from ISS in grayscale
i = cv2.imread('iss006e40544.jpg',0)
img = i[1:1200, 1:2000] # Do some crop under to remove the iss image code

median1 = cv2.medianBlur(img,5)
cv2.imwrite('iss006e40544_median1.png',median1)

median2 = cv2.medianBlur(median1,5)
cv2.imwrite('iss006e40544_median2.png',median2)

ret,thresh1 = cv2.threshold(median2,110,255,cv2.THRESH_BINARY)
cv2.imwrite('iss006e40544_otsu.png',thresh1)

detector = cv2.SimpleBlobDetector()
keypoints = detector.detect(255-thresh1)

for kp in keypoints:
	x, y = kp.pt  
	print (x, y)
	cv2.circle(img,(int(x),int(y)),20 , (255,0,255),1 )

cv2.imwrite('iss006e40544_circles.png',img)

