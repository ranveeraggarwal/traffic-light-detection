from core.feature_extractor import extract_features
from core.test_classifier import test_classifier
from core.train_classifier import train_classifier



# extract_features()
# train_classifier()

image_path = "./data/test_images/test.pgm"
test_classifier(image_path)
