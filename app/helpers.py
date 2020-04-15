import numpy as np
import cv2


threshold = 0.7

im1 = './uploadedImages/testImg.jpg'
im2 = './uploadedImages/testImg.jpg'

def imageMatch(imPath1, imPath2):
    """
        Creates the class.

        Parameters
        ----------

        imPath1:str
            image path of the first image target image
        imPath2:str
            image path of the second image 
        
        Return
        ------
        percent similarity range: [0, 1]
    """

    img1 = cv2.imread(imPath1,0)  # queryImage
    img2 = cv2.imread(imPath2,0) # trainImage

    # Currently using SIFT, but can change
    imageDetector = cv2.xfeatures2d.SIFT_create()

    # Get keypoints
    kp1, des1 = imageDetector.detectAndCompute(img1,None)
    kp2, des2 = imageDetector.detectAndCompute(img2,None)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    # Apply ratio test
    good = []
    percentMatch = 0
    for m,n in matches:
        if m.distance < threshold*n.distance:
            good.append([m])
            goodPoints = len(good)
            percentMatch = goodPoints / len(kp1)
    print("{} % similarity".format(percentMatch * 100))

    return percentMatch

if __name__ == "__main__":
    imageMatch(im1, im2)