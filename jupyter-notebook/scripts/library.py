import matplotlib.pyplot as plt
import sys, traceback
from StringIO import StringIO
from PIL import Image

def process_image_file(image_path):
    print("processing image " + image_path)
    image_fp = StringIO(open(image_path, 'rb').read())
    try:
        image = Image.open(image_fp)
        return process_image(image)
    except IOError:
        return "not found"

def process_image(image, blocks=4):

    if not image.mode == 'RGB':
        print( "Image is not RGB.. converting..")

        # replace alpha channel with white color
        imgg = Image.new('RGB', image.size, (255, 255, 255))
        imgg.paste(image, None)
        image = imgg
        # return None


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
