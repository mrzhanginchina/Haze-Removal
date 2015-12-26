#!/usr/bin/env python
# encoding: utf-8

from PIL import Image
import numpy as np
import math

windowSize = 24
w0 = 0.6
t0 = 0.1

# imageName = "tiananmen1.png"
imageName = "canon3.bmp"
oriImage = np.array(Image.open('images/'+imageName))
imageSize = oriImage.shape

# TODO
# 统计<50的像素所占的比例

darkImage = oriImage.min(axis=2)


maxDarkChannel = darkImage.max()
darkImage = darkImage.astype(np.double)

t = w0 * (darkImage / maxDarkChannel)
T = t * 255
T.dtype = 'uint8'

t[t < t0] = t0

# t = np.array([t, t, t])
J = oriImage
J[:,:,0] = (oriImage[:,:,0] - (1-t) * maxDarkChannel)/t
J[:,:,1] = (oriImage[:,:,1] - (1-t) * maxDarkChannel)/t
J[:,:,2] = (oriImage[:,:,2] - (1-t) * maxDarkChannel)/t

# result = Image.fromarray(J)
# result.show()

def minfilt2(image, windowSize):
    """ Two-dimensional min filter """
    padSize = ((windowSize[0]/2, windowSize[0]/2), (windowSize[0]/2,windowSize[0]/2))
    padImage = np.pad(image, padSize, mode="symmetric")
    minImage = np.zeros_like(image)
    for i in range(len(image)):
        for j in range(len(image[0])):
            minImage[i, j] = padImage[i:i+windowSize[0], j:j+windowSize[1]].min()
    return minImage

dc2 = minfilt2(darkImage, (6, 6))
t = 255 - dc2
t = t / 255
A = min(240, dc2.max())
J[:,:,0] = (oriImage[:,:,0] - (1-t) * A)/t
J[:,:,1] = (oriImage[:,:,1] - (1-t) * A)/t
J[:,:,2] = (oriImage[:,:,2] - (1-t) * A)/t


result = Image.fromarray(J)
result.show()

