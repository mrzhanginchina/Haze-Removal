#!/usr/bin/env python
# encoding: utf-8

from PIL import Image
import numpy as np
from guidedfilter import guidedfilter

def ind2sub(array_shape, ind):
    rows = (ind.astype('int') / array_shape[1])
    cols = (ind.astype('int') % array_shape[1]) # or numpy.mod(ind.astype('int'), array_shape[1])
    return (rows, cols)

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

imageName = "canon3.bmp"
# imageName = "Haze.jpg"
# imageName = "foggy_bench.jpg"
omega = 0.85
r = 80
eps = 10 ** (-3)
t = 0.1

oriImage = Image.open('images/'+imageName)
img = np.array(oriImage).astype(np.double) / 255.0
# numpy rgb2gray don't equal matlab rgb2gray
# grayImage = np.array(oriImage.convert('L')).astype(np.double) / 255.0
grayImage = rgb2gray(img)


imageSize = img.shape
darkImage = img.min(axis=2)

# 滤波
# ordfilt2
(i, j) = ind2sub(darkImage.shape, darkImage.argmax())
A = img[i, j, :].mean()
transmission = 1 - omega * darkImage / A

transmissionFilter = guidedfilter(grayImage, transmission, r, eps )
transmissionFilter[transmissionFilter < t] = t

resultImage = np.zeros_like(img)
for i in range(3):
    resultImage[:, :, i] = (img[:, :, i] - A) / transmissionFilter + A

resultImage[resultImage < 0] = 0
resultImage[resultImage > 1] = 1
result = Image.fromarray((resultImage * 255).astype(np.uint8))
result.show()

