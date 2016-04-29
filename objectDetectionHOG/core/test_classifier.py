import cv2
from skimage.feature import hog
from skimage.io import imread
from skimage.transform import pyramid_gaussian
from sklearn.externals import joblib

from data.config import *

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)


def sliding_window(image, window_size, step_size):
    """
    This function returns a patch of the input image `image` of size equal
    to `window_size`. The first image returned top-left co-ordinates (0, 0)
    and are increment in both x and y directions by the `step_size` supplied.
    So, the input parameters are -
    * `image` - Input Image
    * `window_size` - Size of Sliding Window
    * `step_size` - Incremented Size of Window

    The function returns a tuple -
    (x, y, im_window)
    where
    * x is the top-left x co-ordinate
    * y is the top-left y co-ordinate
    * im_window is the sliding window image
    ---
    :param image:
    :param window_size:
    :param step_size:
    :return:
    """
    for y in xrange(0, image.shape[0], step_size[1]):
        for x in xrange(0, image.shape[1], step_size[0]):
            yield (x, y, image[y:y + window_size[1], x:x + window_size[0]])


def test_classifier(image_path):
    """

    :param image_path:
    :return:
    """
    im = imread(image_path)

    min_wdw_sz = (38, 94)
    step_size = (10, 10)

    model_path = classifier_model_path
    # Load the classifier
    clf = joblib.load(model_path)

    # List to store the detections
    detections = []
    # The current scale of the image
    scale = 0

    downscale = 10000
    visualize_det = False

    # Downscale the image and iterate
    for im_scaled in pyramid_gaussian(im, downscale=downscale):
        # This list contains detections at the current scale
        cd = []
        # If the width or height of the scaled image is less than
        # the width or height of the window, then end the iterations.
        if im_scaled.shape[0] < min_wdw_sz[1] or im_scaled.shape[1] < min_wdw_sz[0]:
            break
        for (x, y, im_window) in sliding_window(im_scaled, min_wdw_sz, step_size):
            if im_window.shape[0] != min_wdw_sz[1] or im_window.shape[1] != min_wdw_sz[0]:
                continue
            # Calculate the HOG features
            fd = hog(image=im_window, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(3, 3), visualise=False)
            prediction = clf.predict(fd.reshape(1, -1))
            if prediction == 1:
                print "Detection:: Location -> ({}, {})".format(x, y)
                print "Scale ->  {} | Confidence Score {} \n".format(scale, clf.decision_function(fd))
                detections.append((x, y, clf.decision_function(fd),
                                   int(min_wdw_sz[0]*(downscale**scale)),
                                   int(min_wdw_sz[1]*(downscale**scale))))
                cd.append(detections[-1])
            # If visualize is set to true, display the working
            # of the sliding window
            if visualize_det:
                clone = im_scaled.copy()
                for x1, y1, _, _, _ in cd:
                    # Draw the detections at this scale
                    cv2.rectangle(clone, (x1, y1), (x1 + im_window.shape[1], y1 +
                                                    im_window.shape[0]), (0, 0, 0), thickness=2)
                cv2.rectangle(clone, (x, y), (x + im_window.shape[1], y +
                                              im_window.shape[0]), (255, 255, 255), thickness=2)
                cv2.imshow("Sliding Window in Progress", clone)
                cv2.waitKey(30)
        # Move the the next scale
        scale += 1

    # Display the results before performing NMS
    # clone = im.copy()

    # good_detections = []
    #
    # for detection in detections:
    #     if detection[2][0] > 1:
    #         good_detections.append(detection)

    # cv2.rectangle(im, (max_detection[0], max_detection[1]),
    # (max_detection[0]+max_detection[3], max_detection[1]+max_detection[4]), (0, 0, 0), thickness=2)

    # detections = good_detections

    print (detections[0][2][0])

    detections = sorted(detections, key=lambda x: x[2][0])

    detections = detections[-10:]

    for (x_tl, y_tl, _, w, h) in detections:
        cv2.rectangle(im, (x_tl, y_tl), (x_tl+w, y_tl+h), (0, 0, 0), thickness=2)
    cv2.imshow("Detections", im)
    cv2.waitKey()
