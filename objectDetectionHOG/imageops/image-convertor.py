import glob
import os

from cv2 import imwrite

from skimage.exposure import rescale_intensity
from skimage.io import imread
from skimage import color

pos_img_path = "../data/train_images/positive_images"
pos_raw = "../data/images_positive"
neg_img_path = "../data/train_images/negative_images"
neg_raw = "../data/images_negative"

if not os.path.isdir(pos_img_path):
    os.makedirs(pos_img_path)

if not os.path.isdir(neg_img_path):
    os.makedirs(neg_img_path)

for im_path in glob.glob(os.path.join(pos_raw, "*")):
    im = imread(im_path)
    im = color.rgb2gray(im)
    im = rescale_intensity(im, out_range=(0, 255))
    image_name = os.path.split(im_path)[1].split(".")[0] + ".pgm"
    image_path = os.path.join(pos_img_path, image_name)
    imwrite(image_path, im)

for im_path in glob.glob(os.path.join(neg_raw, "*")):
    im = imread(im_path, as_grey=True)
    im = color.rgb2gray(im)
    im = rescale_intensity(im, out_range=(0, 255))
    image_name = os.path.split(im_path)[1].split(".")[0] + ".pgm"
    image_path = os.path.join(neg_img_path, image_name)
    imwrite(image_path, im)
