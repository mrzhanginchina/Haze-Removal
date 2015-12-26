#!/usr/bin/env python
# encoding: utf-8

from PIL import Image
import numpy as np

windowSize = 24
w0 = 0.6
t0 = 0.1

imageName = "tiananmen1.png"
imageName = "canon3.bmp"
oriImage = np.array(Image.open('images/'+imageName))
imageSize = oriImage.shape

# TODO
# 统计<50的像素所占的比例

darkImage = oriImage.min(axis=2)
maxDarkChannel = darkImage.max()
darkImage = darkImage.astype(np.double)

t = 1 - w0 * (darkImage / maxDarkChannel)
T = t * 255
T.dtype = 'uint8'

t[t < t0] = t0

# t = np.array([t, t, t])
J = oriImage
J[:,:,0] = (oriImage[:,:,0] - (1-t) * maxDarkChannel)/t
J[:,:,1] = (oriImage[:,:,1] - (1-t) * maxDarkChannel)/t
J[:,:,2] = (oriImage[:,:,2] - (1-t) * maxDarkChannel)/t

result = Image.fromarray(J)
result.show()


