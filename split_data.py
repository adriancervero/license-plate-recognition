from label_converter import ANNOTATIONS_PATH
import os
import shutil
import numpy as np

IMAGES_PATH = 'data/images'
LABELS_PATH = 'data/labels'
TRAIN_IMAGES = 'data/train/images'
TRAIN_LABELS = 'data/train/labels'
VAL_IMAGES = 'data/val/images'
VAL_LABELS = 'data/val/labels'


np.random.seed(42)

list_images = os.listdir(IMAGES_PATH)
list_images = [image.split('.')[0] for image in list_images]
total_count = len(list_images)
split_ind = int(total_count * 0.8)
np.random.shuffle(list_images)

train = list_images[:split_ind]
test = list_images[split_ind:]

for file_name in train:
    image_file = file_name+'.png'
    label_file = file_name+'.txt'
    shutil.copy(os.path.join(IMAGES_PATH, image_file), os.path.join(TRAIN_IMAGES, image_file))
    shutil.copy(os.path.join(LABELS_PATH, label_file), os.path.join(TRAIN_LABELS, label_file))

for file_name in test:
    image_file = file_name+'.png'
    label_file = file_name+'.txt'
    shutil.copy(os.path.join(IMAGES_PATH, image_file), os.path.join(VAL_IMAGES, image_file))
    shutil.copy(os.path.join(LABELS_PATH, label_file), os.path.join(VAL_LABELS, label_file))


print("train size:", len(train))
print("test size:", len(test))

