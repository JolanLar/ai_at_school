# import the opencv library
import cv2
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np


def split_right(arr):
    return arr[int(len(arr) / 2):]


def split_left(arr):
    return arr[:int(len(arr) / 2)]


class Cap:
    def __init__(self):

        # Load the model
        self.model_move = load_model('move.h5')
        self.model_fire = load_model('fire.h5')

        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1.
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # define a video capture object
        self.vid = cv2.VideoCapture(0)
        # vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def norm_and_pred(self, image):
        # Normalize the image
        normalized_image_array = (image.astype(np.float32) / 127.0) - 1
        # Load the image into the array
        self.data[0] = normalized_image_array
        return {
            'fire': np.argmax(self.model_fire.predict(self.data, verbose=0)),
            'move': np.argmax(self.model_move.predict(self.data, verbose=0))
        }

    def predict(self):
        # Capture the video frame
        # by frame
        ret, frame = self.vid.read()
        frame = cv2.flip(frame, 1)

        # Replace this with the path to your image
        image = frame
        # resize the image to a 224x224 with the same strategy as in TM2:
        # resizing the image to be at least 224x224 and then cropping from the center
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_PIL = Image.fromarray(image)
        size = (448, 224)
        image = ImageOps.fit(image_PIL, size, Image.ANTIALIAS)
        image_array = np.asarray(image)

        image_a1 = np.array(list(map(split_right, image_array)))
        cv2.imshow('Player 1', image_a1)
        p1_pred = self.norm_and_pred(image_a1)

        image_a2 = np.array(list(map(split_left, image_array)))
        cv2.imshow('Player 2', image_a2)
        p2_pred = self.norm_and_pred(image_a2)

        cv2.waitKey(1)

        return {
            'p1': p1_pred,
            'p2': p2_pred
        }
