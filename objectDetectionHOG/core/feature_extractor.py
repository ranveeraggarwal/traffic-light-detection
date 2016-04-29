import glob
import os

from skimage.feature import hog
from skimage.io import imread
from sklearn.externals import joblib

from data.config import *
from imageops.progress import update_progress


def extract_features():
    pos_img_path = positive_images_path
    neg_img_path = negative_images_path

    pos_feat_path = positive_features_path
    neg_feat_path = negative_features_path

    if not os.path.isdir(pos_feat_path):
        os.makedirs(pos_feat_path)

    if not os.path.isdir(neg_feat_path):
        os.makedirs(neg_feat_path)

    print "Extracting positive features"
    progress = 0.0
    for im_path in glob.glob(os.path.join(pos_img_path, "*")):
        im = imread(im_path)
        feature_vector = hog(image=im, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(3, 3), visualise=False)
        feature_name = os.path.split(im_path)[1].split(".")[0] + ".feat"
        feature_path = os.path.join(pos_feat_path, feature_name)
        joblib.dump(feature_vector, feature_path)
        progress += 1.0
        update_progress(progress/float(len(glob.glob(os.path.join(pos_img_path, "*")))))

    print "Extracting negative features"
    progress = 0.0
    for im_path in glob.glob(os.path.join(neg_img_path, "*")):
        im = imread(im_path)
        feature_vector = hog(image=im, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(3, 3), visualise=False)
        feature_name = os.path.split(im_path)[1].split(".")[0] + ".feat"
        feature_path = os.path.join(neg_feat_path, feature_name)
        joblib.dump(feature_vector, feature_path)
        progress += 1.0
        update_progress(progress/float(len(glob.glob(os.path.join(neg_img_path, "*")))))


def extract_color_features():
    pass
