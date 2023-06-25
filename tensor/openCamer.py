# import the opencv library
import cv2
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import time

# Load the model
model1 = load_model('keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
  
# define a video capture object
vid = cv2.VideoCapture(0)
#vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
labels = ['Moi',
          'Main',
          'Rien'
        ]


previousLabel = ""


def responseM1(labelName):
    global previousLabel
    
    if (previousLabel == "") :
        previousLabel = labelName   
    elif (previousLabel != labelName):
        print(labelName)
        previousLabel = labelName


counter = 0
thresold = 2
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    frame = cv2.flip(frame,1)
    
    if counter >= thresold:
        # Replace this with the path to your image
        image = frame
        #resize the image to a 224x224 with the same strategy as in TM2:
        #resizing the image to be at least 224x224 and then cropping from the center
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_PIL = Image.fromarray(image)
        size = (224, 224)
        image = ImageOps.fit(image_PIL, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = model1.predict(data,verbose=0)
        
        
        predIdx = np.argmax(prediction)
        
        responseM1(labels[predIdx])
        
        counter = 0
        cv2.imwrite('test_pred'+str(counter)+'.jpg',image_array)
        
    counter += 1

    # Display the resulting frame
    cv2.imshow('frame', frame)
  
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
