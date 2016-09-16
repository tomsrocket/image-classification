from __future__ import print_function
from __future__ import division

import matplotlib.pyplot as plt
from StringIO import StringIO
from PIL import Image # http://effbot.org/imagingbook/image.htm
import os


def get_feature_vector_from_image_file(image_path):

    image_fp = StringIO(open(image_path, 'rb').read())
    image = Image.open(image_fp)
    return calculate_feature_vector(image)


def calculate_feature_vector(image, blocks=4):

    if not image.mode == 'RGB':
        # replace alpha channel with white color
        imgg = Image.new('RGB', image.size, (255, 255, 255))
        imgg.paste(image, None)
        image = imgg

    feature = [0.0] * blocks * blocks * blocks
    pixel_count = 0
    for pixel in image.getdata():
        ridx = int(pixel[0]/(256/blocks))
        gidx = int(pixel[1]/(256/blocks))
        bidx = int(pixel[2]/(256/blocks))
        idx = ridx + gidx * blocks + bidx * blocks * blocks
        feature[idx] += 1
        pixel_count += 1
    return [x/pixel_count for x in feature]


def get_feature_vectors_from_directory(directory):
    '''Returns an array of feature vectors for all the image files in a
    directory (and all its subdirectories). Symbolic links are ignored.

    Args:
      directory (str): directory to process.

    Returns:
      list of list of float: a list of feature vectors.
    '''
    number = 0
    training = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            number = number +1
            file_path = os.path.join(root, file_name)
            print (str(number) + " ", end="")
            print("Processing image " + file_path)
            img_feature = get_feature_vector_from_image_file(file_path)
            if img_feature:
                training.append(img_feature)
    return training
