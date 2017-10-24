#!/usr/bin/env python
# encoding: utf-8

from PIL import Image
from matplotlib import pylab as plt_figure
import numpy as np
import os


def haze_removal(image, w0=0.6, t0=0.1):

    darkImage = image.min(axis=2)
    maxDarkChannel = darkImage.max()
    darkImage = darkImage.astype(np.double)

    t = 1 - w0 * (darkImage / maxDarkChannel)
    T = t * 255
    T.dtype = 'uint8'

    t[t < t0] = t0

    J = image
    J[:, :, 0] = (image[:, :, 0] - (1 - t) * maxDarkChannel) / t
    J[:, :, 1] = (image[:, :, 1] - (1 - t) * maxDarkChannel) / t
    J[:, :, 2] = (image[:, :, 2] - (1 - t) * maxDarkChannel) / t
    result = Image.fromarray(J)

    return result


if __name__ == '__main__':
    list_dir_file = os.walk("./images/")
    list_file = []
    for i in list_dir_file:
        list_file = i[2]

    for i in list_file:
        imageName = i
        file_path = os.path.join("./images", imageName)
        Image.open(file_path).show()
        image_file = np.array(Image.open(file_path))
        image_size = image_file.shape
        result = haze_removal(image_file)
        result.show()
        plt_figure.show()
