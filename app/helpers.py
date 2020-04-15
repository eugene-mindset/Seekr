import numpy as np
import cv2


threshold = 0.7

imPath1 = ''
imPath2 = ''

def imageMatch(imPath1, imPath2)
"""
    Creates the class.

    Parameters
    ----------

    imPath1:str
        image path of the first image
    imPath2:str
        image path of the second image
    
    Return
    ------
    percent similarity range: [0, 1]
"""

img1 = cv2.imread(imPath1,0)  # queryImage
img2 = cv2.imread(imPath2,0) # trainImage

# Initiate SIFT detector
imageDetector = cv2.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = imageDetector.detectAndCompute(img1,None)
kp2, des2 = imageDetector.detectAndCompute(img2,None)

# BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)

# Apply ratio test
good = []
for m,n in matches:
    if m.distance < threshold*n.distance:
        good.append([m])
        a = len(good)
        percent=(a*100)/len(kp2)
    print("{} % similarity".format(percent))
    if percent >= 75.00:
        print('Match Found')
    if percent < 75.00:
        print('Match not Found')
# # cv2.drawMatchesKnn expects list of lists as matches.
# img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,flags=2,outImg=None)

# plt.imshow(img3),plt.show()
# plt.savefig("matplotlib.png") #running in windows subsystem for linux bc no backend