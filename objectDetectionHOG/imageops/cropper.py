import os

import cv2
# from interface.progress import update_progress
from skimage import color
from skimage.exposure import rescale_intensity

pos_img_path = "../data/train_images/positive_images"
neg_img_path = "../data/train_images/negative_images"


class ImageCrop(object):
    def __init__(self, frame, left, top, width, height):
        self.frame = frame
        self.left = int(left)
        self.top = int(top)
        self.width = int(width)
        self.height = int(height)

    def crop_image(self):
        img = cv2.imread(self.frame)
        center_x = self.left + (self.width/2)
        center_y = self.top + (self.height/2)
        up_crop = 85
        down_crop = 86
        left_crop = 35
        right_crop = 35
        height, width = img.shape[:2]
        up_limit = center_y - up_crop
        down_limit = center_y + down_crop
        if up_limit < 0:
            down_limit -= up_limit
            up_limit = 0
        if down_limit > height:
            up_limit += (down_limit - height)
            down_limit = height
        left_limit = center_x - left_crop
        right_limit = center_x + right_crop
        if left_limit < 0:
            right_limit -= left_limit
            left_limit = 0
        if right_limit > width:
            left_limit += (right_limit - width)
            right_limit = width
        cropped_img = img[up_limit: down_limit, left_limit: right_limit]
        return cropped_img


def get_positive_images():
    f = open('../data/image_cropping/crop_locations.txt', 'r')
    f = f.read()

    data = f.split("\n")

    image_crops = []

    for element in data:
        element = element.split(" ")
        if len(element) > 1:
            crop = ImageCrop(frame="../data/frames/" + element[2], left=element[7].strip(","), top=element[10].strip(","),
                             width=element[13].strip(","), height=element[16].strip(","))
            image_crops.append(crop)

    i = 0
    for image_crop in image_crops:
        print i
        cropped_image = image_crop.crop_image()
        image_name = "pos" + str(i) + ".ppm"
        image_path = os.path.join(pos_img_path, image_name)
        cv2.imwrite(image_path, cropped_image)
        i += 1


def get_negative_images():
    f = open('../data/image_cropping/false_locations.txt', 'r')
    f = f.read()

    data = f.split("\n")

    image_crops = []

    for element in data:
        element = element.split(" ")
        if len(element) > 1:
            crop = ImageCrop(frame="../data/allframes/" + str(element[0]) + "/" + str(element[1])+".jpg",
                             left=element[3].strip(","), top=element[5].strip(","), width=35, height=172)
            image_crops.append(crop)

    i = 0
    for image_crop in image_crops:
        print i
        cropped_image = image_crop.crop_image()
        image_name = "neg" + str(i) + ".ppm"
        image_path = os.path.join(neg_img_path, image_name)
        cv2.imwrite(image_path, cropped_image)
        i += 1

get_positive_images()
get_negative_images()
