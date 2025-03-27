from flask import Flask, request, render_template, redirect, url_for

import random

app = Flask(__name__)
global bar_white, bar_black, map_stecs, white_pieses, black_pieses, dies, move, double, impossible_move_Black, impossible_move_White, action, check, point

bar_white = 0
bar_black = 0
map_stecs = []
white_pieses = 15
black_pieses = 15
dies = [0, 0, 0, 0]
move = 0
impossible_move_White = 0
impossible_move_Black = 0
double = 0
check = ""
point = 0


@app.route('/', methods=['GET'])
def Tests_HTML():
    return render_template('html_game.html')


@app.route('/game', methods=['POST'])
def start_game():
    global move, double, check, map_stecs, action
    print(request.__dict__)
    action = request.data.decode('utf-8')
    if action == "Start game":
        if map_stecs != []:
            return "The game has already begun."
        else:
            chekcers_moves = 24
            for i in range(0, chekcers_moves):
                map_stecs.append([])
            for i in range(0, 16):
                map_stecs[0].append('Black pies')
                map_stecs[-1].append('White pies')
            return "Map is done." + str(len(map_stecs)) + str(len(map_stecs[0]))
    elif action == 'Transition move':
        move += 1
        if move % 2 == 0:
            check = "White pies"
        else:
            check = "Black pies"
        dies[0] = random.randint(1, 6)
        dies[1] = random.randint(1, 6)
        dies[2] = 0
        dies[3] = 0
        if dies[0] == dies[1]:
            dies[2] = dies[0]
            dies[3] = dies[0]
            double += 1
            return str(dies[0]) + ' ' + str(dies[1]) + ' ' + str(dies[2]) + ' ' + str(
                dies[3]) + ' ' + "A double has been rolled, movex2."
        else:
            return str(dies[0]) + ' ' + str(dies[1]) + ' '
    elif action == "Give up":
        if check == "White pies":
            return "Black win"
        else:
            return "White win"
    else:
        return "Unknown action"


@app.route('/game/move', methods=['POST'])
def game():  # player say the colum of the pies
    global bar_white, bar_black, map_stecs, white_pieses, black_pieses, dies, move, double, impossible_move_Black, impossible_move_White, action, check, point
    point = int(request.data.decode('utf-8'))
    if not map_stecs[point - 1]:
        if move % 2 == 0:
            impossible_move_White += 1
        else:
            impossible_move_Black += 1
        if impossible_move_White == 2 or impossible_move_Black == 2:
            return "Game is over. Impossible moves"
        else:
            return "Impossible move"
    elif map_stecs[point - 1][-1] != check:
        if move % 2 == 0:
            impossible_move_White += 1
        else:
            impossible_move_Black += 1
        if impossible_move_White == 2 or impossible_move_Black == 2:
            return "Game is over. Impossible moves"
        else:
            return "Impossible move"
    else:
        return "ERROR"  # else: go to /game/move/dice


@app.route('/game/move/dice', methods=['GET'])
def game_move():
    global bar_white, bar_black, map_stecs, white_pieses, black_pieses, dies, move, double, impossible_move_Black, impossible_move_White, action, check, point
    dies_move_str = (request.data.decode('utf-8'))  # player pick what dies he will play.
    dies_move = 0
    if len(dies_move_str) > 1:
        for i in range(0, len(dies_move_str)):
            dies_move += dies[i]
    elif len(dies_move_str) > 4:
        return "There is only two dies"
    else:
        dies_move = dies[int(dies_move_str)]
    if not map_stecs[point - 1 + dies_move]:
        map_stecs.pop([point - 1][-1])  # OK
        map_stecs[point - 1 + dies_move].append(str(check))
        return "Move is done" + str(len(map_stecs[point - 1 + dies_move]))

    elif map_stecs[point - 1 + dies_move][-1] != check:
        if check == "Black pies":
            impossible_move_Black += 1  # OK
            return "Impossible move"
        else:
            impossible_move_White += 1
            return "Impossible move"  # come back to start of /game/move
    else:
        map_stecs[point - 1 + dies_move].append(str(check))
        map_stecs.pop([point - 1][-1])
        return "Move is done" + str(len(map_stecs[point - 1 + dies_move]))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
