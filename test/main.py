import cv2
from PIL import Image, ImageOps
import numpy as np

vid = cv2.VideoCapture(0)
ret, frame = vid.read()
frame = cv2.flip(frame, 1)

image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
image_PIL = Image.fromarray(image)
size = (448, 224)
image = ImageOps.fit(image_PIL, size, Image.ANTIALIAS)
image_array = np.asarray(image)


# image_a1 = image_array[0:int(len(image_array)/2)]

def split_right(arr):
    return arr[int(len(arr)/2):]


def split_left(arr):
    return arr[:int(len(arr)/2)]

image_a1 = np.array(list(map(split_right, image_array)))
image_a2 = np.array(list(map(split_left, image_array)))

cv2.imshow('image', image_a1)
cv2.waitKey(0)
cv2.imshow('image', image_a2)
cv2.waitKey(0)

