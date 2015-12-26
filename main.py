#!/usr/bin/env python
# encoding: utf-8

""" https://github.com/akutta/Haze-Removal """

from PIL import Image
import numpy as np
import math

windowSize = 24
imageName = "tiananmen1.png"
oriImage = np.array(Image.open('images/'+imageName))/255
imageSize = oriImage.shape


def makeDarkChannel(image, windowSize):
    padImage = np.pad(image, ((windowSize/2, windowSize/2), (windowSize/2, windowSize/2), (0, 0)), mode='symmetric')
    darkChannelImage = np.zeros(imageSize[:2], dtype='float')
    for i in range(imageSize[0]):
        for j in range(imageSize[1]):
            darkChannelImage[i,j] = padImage[i:i+windowSize, j:j+windowSize].min()
    return darkChannelImage

numBrightestPixel = math.ceil(0.001 * imageSize[0] * imageSize[1])

