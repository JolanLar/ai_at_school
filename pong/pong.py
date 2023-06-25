# Import required library
import turtle, joblib, os.path
from sklearn.neural_network import MLPClassifier

modelPath = 'model.clf'

# Create screen
sc = turtle.Screen()
sc.title("Pong game")
sc.bgcolor("white")
sc.setup(width=1000, height=600)

# Left paddle
left_pad = turtle.Turtle()
left_pad.speed(0)
left_pad.shape("square")
left_pad.color("black")
left_pad.shapesize(stretch_wid=6, stretch_len=2)
left_pad.penup()
left_pad.goto(-400, 0)

# Right paddle
right_pad = turtle.Turtle()
right_pad.speed(0)
right_pad.shape("square")
right_pad.color("black")
right_pad.shapesize(stretch_wid=6, stretch_len=2)
right_pad.penup()
right_pad.goto(400, 0)

# Ball of circle shape
hit_ball = turtle.Turtle()
hit_ball.speed(40)
hit_ball.shape("circle")
hit_ball.color("blue")
hit_ball.penup()
hit_ball.goto(0, 0)
hit_ball.dx = 5
hit_ball.dy = -5

# Initialize the score
left_player = 0
right_player = 0

# Displays the score
sketch = turtle.Turtle()
sketch.speed(0)
sketch.color("blue")
sketch.penup()
sketch.hideturtle()
sketch.goto(0, 260)
sketch.write("Left_player : 0    Right_player: 0",
             align="center", font=("Courier", 24, "normal"))


# Functions to move paddle vertically
def paddleaup():
    global currentAAction
    y = left_pad.ycor()
    if y < 230:
        y += 20
        left_pad.sety(y)
        currentAAction = 1


def paddleadown():
    global currentAAction
    y = left_pad.ycor()
    if y > -230:
        y -= 20
        left_pad.sety(y)
        currentAAction = 1


def paddlebup():
    global currentBAction
    y = right_pad.ycor()
    if y < 230:
        y += 20
        right_pad.sety(y)
        currentBAction = 1


def paddlebdown():
    global currentBAction
    y = right_pad.ycor()
    if y > -230:
        y -= 20
        right_pad.sety(y)
        currentBAction = 2


def releasedBKey():
    global currentBAction
    currentBAction = 0

def releasedAKey():
    global currentAAction
    currentAAction = 0


def train():
    global isTraining, X, y, clf
    isTraining = True
    print("Train")
    print(X)
    print(y)
    clf.fit(X, y)
    X, y = [], []
    joblib.dump(clf, modelPath)
    isTraining = False


def autoPlay():
    global clf, autoPlay
    autoPlay = not autoPlay


# Keyboard bindings
sc.listen()
sc.onkeypress(autoPlay, "p")
sc.onkeypress(train, "t")

sc.onkeypress(paddleaup, "e")
sc.onkeypress(paddleadown, "x")
sc.onkeyrelease(releasedAKey, "Up")
sc.onkeyrelease(releasedAKey, "Down")

sc.onkeypress(paddlebup, "Up")
sc.onkeypress(paddlebdown, "Down")
sc.onkeyrelease(releasedBKey, "Up")
sc.onkeyrelease(releasedBKey, "Down")

isTraining = False
autoPlay = False

if os.path.exists(modelPath):
    clf = joblib.load(modelPath)
else:
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(150,), random_state=1, max_iter=5000,
                        n_iter_no_change=15, verbose=False)

X = []
y = []

currentRecord = []
currentAAction = 0  # UP = 1, Down = 2, None = 0
currentBAction = 0  # UP = 1, Down = 2, None = 0
# ballOldXY = [0, 0]

while True:
    sc.update()
    hit_ball.setx(hit_ball.xcor() + hit_ball.dx)
    hit_ball.sety(hit_ball.ycor() + hit_ball.dy)

    if isTraining == False:
        # currentRecord = [right_pad.ycor(), hit_ball.xcor(), hit_ball.ycor()] + ballOldXY
        # currentRecord = [(1, 2)[hit_ball.ycor() > right_pad.ycor()]]

        # Record format = [ball-direction-x-to-pad, ball-direction-y, x-distance-between-ball-and-pad,
        # y-distance-between-ball-and-pad]
        currentARecord = [-hit_ball.dx, hit_ball.dy, abs(left_pad.xcor() - hit_ball.xcor()),
                          hit_ball.ycor() - left_pad.ycor()]
        currentBRecord = [hit_ball.dx, hit_ball.dy, abs(right_pad.xcor() - hit_ball.xcor()),
                          hit_ball.ycor() - right_pad.ycor()]

        if autoPlay:
            predA = clf.predict([currentARecord])
            if predA == 1:
                paddleaup()
            elif predA == 2:
                paddleadown()
            predB = clf.predict([currentBRecord])
            if predB == 1:
                paddlebup()
            elif predB == 2:
                paddlebdown()
            # print("A:",currentARecord, predA[0], "  B:",currentBRecord, predB[0])
        else:
            X.append(currentBRecord)
            y.append(currentBAction)
            X.append(currentARecord)
            y.append(currentAAction)

        # ballOldXY = [hit_ball.xcor(), hit_ball.ycor()]

    # Checking borders
    if hit_ball.ycor() > 280:
        hit_ball.sety(280)
        hit_ball.dy *= -1

    if hit_ball.ycor() < -280:
        hit_ball.sety(-280)
        hit_ball.dy *= -1

    if hit_ball.xcor() > 500:
        hit_ball.goto(0, 0)
        hit_ball.dy *= -1
        left_player += 1
        sketch.clear()
        sketch.write("Left_player : {}    Right_player: {}".format(
            left_player, right_player), align="center",
            font=("Courier", 24, "normal"))

    if hit_ball.xcor() < -500:
        hit_ball.goto(0, 0)
        hit_ball.dy *= -1
        right_player += 1
        sketch.clear()
        sketch.write("Left_player : {}    Right_player: {}".format(
            left_player, right_player), align="center",
            font=("Courier", 24, "normal"))

    # Paddle ball collision
    if (hit_ball.xcor() > 360 and hit_ball.xcor() < 370) and (
            hit_ball.ycor() < right_pad.ycor() + 80 and hit_ball.ycor() > right_pad.ycor() - 80):
        hit_ball.setx(360)
        hit_ball.dx *= -1

    if (hit_ball.xcor() < -360 and hit_ball.xcor() > -370) and (
            hit_ball.ycor() < left_pad.ycor() + 80 and hit_ball.ycor() > left_pad.ycor() - 80):
        hit_ball.setx(-360)
        hit_ball.dx *= -1
