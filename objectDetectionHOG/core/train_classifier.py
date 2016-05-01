import glob
import os

import numpy
from sklearn.externals import joblib
from sklearn.svm import LinearSVC

from data.config import *


def train_classifier():
    pos_feat_path = positive_features_path
    neg_feat_path = negative_features_path

    model_path = classifier_model_path

    feature_vectors = []
    labels = []

    for feat_path in glob.glob(os.path.join(pos_feat_path, "*.feat")):
        fd = joblib.load(feat_path)
        print len(fd)
        if len(fd):
            fd = fd.astype(numpy.object)
            feature_vectors.append(fd)
            labels.append(1)

    for feat_path in glob.glob(os.path.join(neg_feat_path, "*.feat")):
        fd = joblib.load(feat_path)
        print len(fd)
        if len(fd):
            fd = fd.astype(numpy.object)
            feature_vectors.append(fd)
            labels.append(0)

    classifier = LinearSVC()
    print "Training classifier"
    classifier.fit(feature_vectors, labels)
    print "Classifier successfully trained"
    if not os.path.isdir(os.path.split(model_path)[0]):
        os.makedirs(os.path.split(model_path)[0])
    joblib.dump(classifier, model_path)
