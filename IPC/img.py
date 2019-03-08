import csv
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
import cv2
	
img_data = genfromtxt("screen_img.csv", delimiter=',', dtype = int)

print(img_data.shape)

RGB = []
for i in range(0, 240):
	row = []
	for j in range(0, 320):
		row.append([img_data[i, j*3], img_data[i, j*3+1], img_data[i, j*3+2]])
	RGB.append(row)

np.asarray(RGB)
RGB = np.flip(RGB, 0)
plt.imshow(RGB)
plt.show()

# 640, 480, 3
# 640+1, 480*3+1
