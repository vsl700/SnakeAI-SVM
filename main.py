# Simple Snake Game in Python 3 for Beginners
# By @TokyoEdTech
#
# AI Experiment by VASCii (vsl700 on GitHub) 2022/05

import turtle
import time
import random
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import svm_ai_container as agent


delay = 0.1

# Score
score = 0
high_score = 0

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game by @TokyoEdTech")
wn.bgcolor("green")
wn.setup(width=600, height=600)
wn.tracer(0)  # Turns off the screen updates

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

gen = 0

w = a = s = d = False
turn = False


# Functions
def go_up():
    if turn:
        return

    global w
    global a
    global s
    global d

    w = True
    a = s = d = False
    agent.append_data(head.xcor(), head.ycor(), len(segments), food.xcor(), food.ycor(), head.direction, w, a, s, d)

    dir_up()


def dir_up():
    global turn

    if turn:
        return

    if head.direction != "down":
        head.direction = "up"

    turn = True


def go_down():
    if turn:
        return

    global w
    global a
    global s
    global d

    s = True
    w = a = d = False
    agent.append_data(head.xcor(), head.ycor(), len(segments), food.xcor(), food.ycor(), head.direction, w, a, s, d)

    dir_down()


def dir_down():
    global turn

    if turn:
        return

    if head.direction != "up":
        head.direction = "down"

    turn = True


def go_left():
    if turn:
        return

    global w
    global a
    global s
    global d

    a = True
    w = s = d = False
    agent.append_data(head.xcor(), head.ycor(), len(segments), food.xcor(), food.ycor(), head.direction, w, a, s, d)

    dir_left()


def dir_left():
    global turn
    if turn:
        return

    if head.direction != "right":
        head.direction = "left"

    turn = True


def go_right():
    if turn:
        return

    global w
    global a
    global s
    global d

    d = True
    w = a = s = False
    agent.append_data(head.xcor(), head.ycor(), len(segments), food.xcor(), food.ycor(), head.direction, w, a, s, d)

    dir_right()


def dir_right():
    global turn
    if turn:
        return

    if head.direction != "left":
        head.direction = "right"

    turn = True


def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

    global turn
    turn = False


def turn_on_gaming_mode():
    global gaming_mode
    gaming_mode = True


def game_over():
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "stop"

    # Hide the segments
    for segment in segments:
        segment.goto(1000, 1000)

    # Clear the segments list
    segments.clear()

    # Transit between learning and gaming
    agent.fit()
    global gaming_mode
    gaming_mode = True

    # Reset the score
    global score
    score = 0

    # Reset the delay
    global delay
    delay = 0.1

    pen.clear()
    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    global gen
    gen = gen + 1
    print(gen)
    print(np.size(agent.x, 0))

    # Show some interesting graphs
    # cmap = sns.cubehelix_palette(as_cmap=True)
    # f, ax = plt.subplots()
    # points = ax.scatter(
    #     np.array(agent.x)[:, 0], np.array(agent.x)[:, 1], c=np.array(agent.y)[0], s=50, cmap=cmap
    # )
    # f.colorbar(points)
    #
    # f, ax = plt.subplots()
    # points = ax.scatter(
    #     np.array(agent.x)[:, 0], np.array(agent.x)[:, 1], c=np.array(agent.y)[1], s=50, cmap=cmap
    # )
    # f.colorbar(points)
    #
    # f, ax = plt.subplots()
    # points = ax.scatter(
    #     np.array(agent.x)[:, 0], np.array(agent.x)[:, 1], c=np.array(agent.y)[2], s=50, cmap=cmap
    # )
    # f.colorbar(points)
    #
    # f, ax = plt.subplots()
    # points = ax.scatter(
    #     np.array(agent.x)[:, 0], np.array(agent.x)[:, 1], c=np.array(agent.y)[3], s=50, cmap=cmap
    # )
    # f.colorbar(points)
    # plt.show()


# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(turn_on_gaming_mode, "space")

gaming_mode = False

# Main game loop
while True:
    wn.update()

    if gaming_mode:
        direction = agent.predict_data(head.xcor(), head.ycor(), len(segments), food.xcor(), food.ycor(), head.direction)
        if direction == "up":
            dir_up()
        elif direction == "down":
            dir_down()
        elif direction == "left":
            dir_left()
        elif direction == "right":
            dir_right()
    else:
        agent.append_data(head.xcor(), head.ycor(), len(segments), food.xcor(), food.ycor(), head.direction, w, a, s, d)

    # Check for a collision with the border
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        game_over()

    # Check for a collision with the food
    if head.distance(food) < 20:
        # Move the food to a random spot
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)

        # Shorten the delay
        delay -= 0.001

        # Increase the score
        score += 10

        if score > high_score:
            high_score = score

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

        # Move the end segments first in reverse order
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # Check for head collision with the body segments
    for segment in segments:
        if segment.distance(head) < 20:
            game_over()

    time.sleep(delay)

wn.mainloop()
