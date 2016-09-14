import matplotlib.pyplot as plt
from StringIO import StringIO
from PIL import Image # http://effbot.org/imagingbook/image.htm


def get_feature_vector_from_image_file(image_path):

    print("Processing image " + image_path)
    image_fp = StringIO(open(image_path, 'rb').read())
    image = Image.open(image_fp)
    return calculate_feature_vector(image)


def calculate_feature_vector(image, blocks=4):

    if not image.mode == 'RGB':
        print( "Image is not RGB.. converting..")

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
