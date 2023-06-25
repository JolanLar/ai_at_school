# import the opencv library
import cv2
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np


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
        size = (224, 224)
        image = ImageOps.fit(image_PIL, size, Image.ANTIALIAS)
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # Load the image into the array
        self.data[0] = normalized_image_array
        prediction_p1_fire = self.model_fire.predict(self.data, verbose=0)
        prediction_p1_move = self.model_move.predict(self.data, verbose=0)

        return {
            'move': np.argmax(prediction_p1_move),
            'fire': np.argmax(prediction_p1_fire)
        }
