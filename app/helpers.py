import numpy as np
import cv2
# from matplotlib import pyplot as plt


threshold = 0.85

# im1 = './testImages/iphon11p2.jpg'
# im2 = './testImages/iphone11.jpg'
IMAGE_FOLDER = './uploadedImages/'

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

    img1 = cv2.imread(IMAGE_FOLDER + imPath1,0)  # queryImage
    img2 = cv2.imread(IMAGE_FOLDER + imPath2,0) # trainImage
    #print("image one path: " + str(imPath1))
    #print("image two path: " + str(imPath2))

    # Currently using SIFT, but can change
    imageDetector = cv2.xfeatures2d.SIFT_create()

    # Get keypoints
    kp1, des1 = imageDetector.detectAndCompute(img1,None)
    kp2, des2 = imageDetector.detectAndCompute(img2,None)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    # Apply ratio test
    countGood = 0
    for m,n in matches:
        if m.distance < threshold*n.distance:
            countGood += 1
    print(countGood)
    # print("{} % similarity".format(percentMatch * 100))
    # cv2.drawMatchesKnn expects list of lists as matches.
    # img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,flags=2,outImg=None)

    # plt.imshow(img3),plt.show()
    # plt.savefig("matplotlib.png") #running in windows subsystem for linux bc no backend 

    return countGood

# if __name__ == "__main__":
#     imageMatch(im1, im2)
