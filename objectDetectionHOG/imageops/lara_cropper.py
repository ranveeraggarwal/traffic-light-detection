import os

import random

import cv2

# from skimage import color
# from skimage.exposure import rescale_intensity

from progress import update_progress

f = open('../lara_data/ground_truth.txt', 'r')
f = f.read()
data = f.split('\n')

pos_img_path = "./train_images/positive_images"
neg_img_path = "./train_images/negative_images"

max_window_size = [0, 0]

positive_data = []

for data_point in data:
    data_point = data_point.split()
    frame_number = data_point[2]
    x1 = data_point[3]
    y1 = data_point[4]
    x2 = data_point[5]
    y2 = data_point[6]
    if abs(int(x2) - int(x1)) > max_window_size[0]:
        max_window_size[0] = abs(int(x2) - int(x1))
    if abs(int(y2) - int(y1)) > max_window_size[1]:
        max_window_size[1] = abs(int(y2) - int(y1))
    # As of now, we ignore the other data attributes since we only need traffic lights
    frame = 'frame_' + '0'*(6-len(frame_number)) + frame_number + '.jpg'
    frame_data = [frame, x1, y1, x2, y2]
    positive_data.append(frame_data)

if max_window_size[0] % 2 == 1:
    max_window_size[0] += 1

if max_window_size[1] % 2 == 1:
    max_window_size[1] += 1


def gen_pos():

    progress = 0.0

    cropped_images = []

    print("Cropping Images")

    for data_point in positive_data:
        img = cv2.imread("../lara_data/images/" + data_point[0])
        height, width = img.shape[:2]
        up_limit = (int(data_point[2]) + int(data_point[4]))/2 - max_window_size[1]/2
        down_limit = (int(data_point[2]) + int(data_point[4]))/2 + max_window_size[1]/2
        if up_limit < 0:
            down_limit -= up_limit
            up_limit = 0
        if down_limit > height:
            up_limit += (down_limit - height)
            down_limit = height
        left_limit = (int(data_point[1]) + int(data_point[3]))/2 - max_window_size[0]/2
        right_limit = (int(data_point[1]) + int(data_point[3]))/2 + max_window_size[0]/2
        if left_limit < 0:
            right_limit -= left_limit
            left_limit = 0
        if right_limit > width:
            left_limit += (right_limit - width)
            right_limit = width
        cropped_img = img[up_limit: down_limit, left_limit: right_limit]
        h, w = cropped_img.shape[:2]
        if int(w) == int(max_window_size[0]) and int(h) == int(max_window_size[1]):
            cropped_images.append(cropped_img)
        progress += 1.0
        update_progress(progress/float(len(data)))

    print("Generating Positive Images")

    progress = 0.0

    i = 0
    for cropped_image in cropped_images:
        # out_image = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2YCR_CB)
        # out_image = cv2.split(out_image)[0]
        out_image = cropped_image
        image_name = "pos" + str(i) + ".ppm"
        image_path = os.path.join(pos_img_path, image_name)
        cv2.imwrite(image_path, out_image)
        progress += 1.0
        i += 1
        update_progress(progress/float(len(cropped_images)))


def gen_neg():
    progress = 0.0
    cropped_images = []
    for i in range(9000):
        frame_number = str(random.randint(0, 11178))
        frame = 'frame_' + '0'*(6-len(frame_number)) + frame_number + '.jpg'
        img = cv2.imread("../lara_data/images/" + frame)
        height, width = img.shape[:2]
        x = random.randint(max_window_size[0], width - max_window_size[0])
        y = random.randint(max_window_size[1], height - max_window_size[1])
        up_limit = y - max_window_size[1]/2
        down_limit = y + max_window_size[1]/2
        left_limit = x - max_window_size[0]/2
        right_limit = x + max_window_size[0]/2
        cropped_img = img[up_limit: down_limit, left_limit: right_limit]
        h, w = cropped_img.shape[:2]
        if int(w) == int(max_window_size[0]) and int(h) == int(max_window_size[1]):
            cropped_images.append(cropped_img)
        progress += 1.0
        update_progress(progress/float(9000))

    print("Generating Negative Images")

    progress = 0.0

    i = 0
    for cropped_image in cropped_images:
        # out_image = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2YCR_CB)
        # out_image = cv2.split(out_image)[0]
        out_image = cropped_image
        image_name = "neg" + str(i) + ".ppm"
        image_path = os.path.join(neg_img_path, image_name)
        cv2.imwrite(image_path, out_image)
        progress += 1.0
        i += 1
        update_progress(progress/float(len(cropped_images)))

gen_pos()
gen_neg()
