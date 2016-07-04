############################################################################
# This file is only an example of the star detection procedure that will   #
# take place                     					   #
############################################################################

import numpy as np
import cv2
import math
import startracker_lib
# Load an example image from ISS in grayscale
# http://spaceflight.nasa.gov/gallery/images/station/crew-6/hires/iss006e40544.jpg

filename='bigdipper_carboni_f'
#filename='starfield'

img = cv2.imread('images/'+filename+'.jpg',0)

# img = i[1:1200, 1:2000] # Do some crop under to remove the iss image code

median1 = cv2.medianBlur(img,5)
cv2.imwrite('output/'+filename+'_median1.png',median1)

median2 = cv2.medianBlur(median1,5)
cv2.imwrite('output/'+filename+'_median2.png',median2)

ret,thresh1 = cv2.threshold(median2,110,255,cv2.THRESH_BINARY)
cv2.imwrite('output'+filename+'_otsu.png',thresh1)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Filter by Area.
params.filterByArea = True
params.minArea = 12

detector = cv2.SimpleBlobDetector(params)
keypoints = detector.detect(255-thresh1)

# Draw detections on image
font = cv2.FONT_HERSHEY_SIMPLEX
for s,kp in enumerate(keypoints):
	x, y = kp.pt
	#print (x, y)
	cv2.circle(img,(int(x),int(y)),20 , (255,0,255),1 )
	cv2.putText(img,str(s),(int(x)-22,int(y)-22), font, 0.6,(255,255,255))
cv2.imwrite('output/'+filename+'_circles.png',img)


print startracker_lib.imgGetAngles(img, 30, 40)
pairs=startracker_lib.create_pairs(keypoints, 6, 35, 8745.1)
print startracker_lib.query(pairs, 0.046)
