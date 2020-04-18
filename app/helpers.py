from base64 import standard_b64decode
import cv2
import numpy as np


threshold = 0.85

def imageMatch(item1, item2):
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

    # Don't compute match at all if one of the items has no images
    if not item1.images or not item2.images:
        return 100

    # Pairwise compare all of item1's images with item2's images, return highest
    # number of matches found between the images of the two items
    max_matches = 0

    for img1 in item1.images:
        # Convert from base64 string to an actual image
        img1_bytes = standard_b64decode(img1.imageData)
        img1_data = cv2.imdecode(np.frombuffer(img1_bytes, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

        for img2 in item2.images:
            # Convert from base64 string to an actual image
            img2_bytes = standard_b64decode(img2.imageData)
            img2_data = cv2.imdecode(np.frombuffer(img2_bytes, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

            # Currently using SIFT, but can change
            imageDetector = cv2.xfeatures2d.SIFT_create()

            # Get keypoints and descriptors
            kp1, des1 = imageDetector.detectAndCompute(img1_data,None)
            kp2, des2 = imageDetector.detectAndCompute(img2_data,None)

            # BFMatcher with default params
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1,des2, k=2)

            # Apply ratio test
            countGood = 0
            for m,n in matches:
                if m.distance < threshold*n.distance:
                    countGood += 1
            
            if countGood > max_matches:
                max_matches = countGood

    return max_matches
