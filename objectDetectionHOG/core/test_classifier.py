import cv2
from skimage.feature import hog
from skimage.io import imread
from sklearn.externals import joblib

from data.config import *


def get_regions(roi_path):
    f = open(roi_path, 'r').read()
    f = f.split("\n")
    f = [i.split() for i in f]
    return f


def test_classifier(img_path, roi_path):
    model_path = classifier_model_path
    # Load the classifier
    clf = joblib.load(model_path)

    max_win_y = 171
    max_win_x = 70

    detections = []

    regions = get_regions(roi_path)

    im = imread(img_path)
    im_ycbcr = cv2.cvtColor(im, cv2.COLOR_RGB2YCR_CB)
    im = cv2.split(im_ycbcr)[0]

    for region in regions:
        x = int(float(region[0])*1000)
        y = int(float(region[1])*1000)

        im_window = im[y: y + max_win_y, x: x + max_win_x]

        fd = hog(image=im_window, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(3, 3), visualise=False)

        if len(fd) == 9234:
            prediction = clf.predict(fd.reshape(1, -1))

            if prediction == 1:
                print "Detection:: Location -> ({}, {})".format(x, y)
                print "Confidence Score {} \n".format(clf.decision_function(fd))
                detections.append((x, y, clf.decision_function(fd)))

    im = imread(img_path)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    for (x_tl, y_tl, _) in detections:
        cv2.rectangle(im, (x_tl, y_tl), (x_tl+max_win_x, y_tl+max_win_y), (0, 255, 0), thickness=1)
    cv2.imwrite("result.png", im)
