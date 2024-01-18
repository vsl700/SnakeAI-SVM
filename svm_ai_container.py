from sklearn import svm
import csv

clf = [svm.SVC(kernel="poly") for i in range(4)]
x = []
y = [[] for i in range(len(clf))]
csv_data = []


def fit():
    for i in range(len(clf)):
        clf[i].fit(x, y[i])


def dir_to_int(direction):
    if direction == "up":
        return 0
    if direction == "left":
        return 1
    if direction == "down":
        return 2
    if direction == "right":
        return 3


def append_data(snake_x, snake_y, length, food_x, food_y, direction,
                w_press=False, a_press=False, s_press=False, d_press=False):
    if direction == "stop":
        return

    arr_x = [snake_x, snake_y, length, food_x, food_y, dir_to_int(direction)]
    x.append(arr_x)

    arr_y = [w_press, a_press, s_press, d_press]
    for i in range(len(arr_y)):
        y[i].append(1) if arr_y[i] else y[i].append(0)

    directions = ["up", "left", "down", "right"]
    out_dir = [""]
    for i in range(len(directions)):
        if arr_y[i]:
            out_dir = [directions[i]]
            break

    arr_csv = arr_x + out_dir
    csv_data.append(arr_csv)


def predict_data(snake_x, snake_y, length, food_x, food_y, direction):
    if direction == "stop":
        return "left"

    arr_x = [snake_x, snake_y, length, food_x, food_y, dir_to_int(direction)]
    arr_predict = [i.predict([arr_x]) for i in clf]

    directions = ["up", "left", "down", "right"]
    for i in range(len(directions)):
        if arr_predict[i] == 1:
            return directions[i]

    return "none"


def save_to_file():
    with open('data.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
