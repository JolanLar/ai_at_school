import cv2
from sklearn.neural_network import MLPClassifier
from joblib import dump, load


X = []
y = []


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized
    

def convertImg(im,expectedRes):
    grayImage = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 250, 255, cv2.THRESH_BINARY)
    image = image_resize(blackAndWhiteImage, height = 20)
    image[image<254] = 0
    image[image>254] = 1
    inputData = image.flatten()
    X.append(inputData)
    y.append(expectedRes)
    

def load_files():
    print("load files")
    for i in range(0,3):
        for j in range(0,6):
            fileName = "{sample}_{record}.png".format(sample = i, record = j)
            print(fileName)
            im = cv2.imread(fileName)
            convertImg(im,i)
    
def trainModel(samples,responses):
    print(samples,responses)
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(20, 20), random_state=1)
    clf.fit(samples, responses)
    dump(clf, 'clf.joblib') 
    

load_files()
trainModel(X,y)














