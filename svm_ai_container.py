from sklearn import svm


clf = [svm.SVC(kernel="poly", degree=5) for i in range(4)]
x = []
y = [[] for i in range(len(clf))]


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
