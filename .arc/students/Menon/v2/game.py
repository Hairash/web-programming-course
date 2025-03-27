# Unused imports
from dataclasses import dataclass
from flask import Flask, request, render_template, redirect, url_for

import random

app = Flask(__name__)
# Bad style, better to use object
global bar_white, bar_black, map_stecs, white_checkers, black_checkers, dice, move, double, impossible_move_Black, impossible_move_White, action, checkers, point


# @dataclass
# class GlobalVars:
bar_white = 0
bar_black = 0
map_stecs = []
white_checkers = 0
black_checkers = 0
dice = [0, 0, 0, 0]
move = 0
impossible_move_White = 0
impossible_move_Black = 0
double = 0
checkers = ""
point = 0


@app.route('/', methods=['GET'])
# Style
def Tests_HTML():
    return render_template('Tests_HTML.html')


@app.route('/game', methods=["POST"])
def start_game():
    global move, double, checkers, map_stecs, action, black_checkers, white_checkers
    action = request.form.get("tasks")
    # WOW!
    if action[:10] == "Start game":
        if map_stecs:
            return "The game has already begun."
        else:
            action_move = action.split(' ')
            checkers_moves = int(action_move[2])  #map size
            checkers_quantity = int(action_move[3])  #checkers quantity
            for i in range(0, checkers_moves):
                map_stecs.append([])
            for i in range(0, checkers_quantity):
                white_checkers +=1
                black_checkers +=1
                map_stecs[0].append('Black pies')
                map_stecs[-1].append('White pies')
            # Better to use template with parameters
            return render_template(
                'move.html',
                message="Map is done.",
                size=str(len(map_stecs)),
                checkers=str(len(map_stecs[0])),
            )
    elif action == 'Transition move':
        move += 1
        if move % 2 == 0:
            checkers = "White pies"
        else:
            checkers = "Black pies"
        dice = [random.randint(1, 6), random.randint(1, 6)]
        # dice[0] = random.randint(1, 6)
        # dice[1] = random.randint(1, 6)
        # dice[2] = 0
        # dice[3] = 0
        if dice[0] == dice[1]:
            dice = dice * 2
            # dice.append(random.randint(1, 6))
            # dice.append(random.randint(1, 6))
            # dice[2] = dice[0]
            # dice[3] = dice[0]
            double += 1
            return str(dice[0]) + ' ' + str(dice[1]) + ' ' + str(dice[2]) + ' ' + str(
                dice[3]) + ' ' + "A double has been rolled, movex2." + render_template('move.html')
        else:
            return str(dice[0]) + ' ' + str(dice[1]) + render_template('move.html')
    elif action == "Give up":
        if checkers == "White pies":
            return "Black win"
        else:
            return "White win"
    else:
        return "Unknown action"

def checker_exists(pos):
    return not map_stecs[int(point) - 1]


@app.route('/game/move', methods=['POST'])
def game():  # player say the colum of the pies
    # Terrible
    global bar_white, bar_black, map_stecs, white_checkers, black_checkers, dies, move, double, impossible_move_Black, impossible_move_White, checkers, point
    point = request.form.get('game')
    print('====>', map_stecs)
    if checker_exists(int(point) - 1):
        if move % 2 == 0:
            impossible_move_White += 1
        else:
            impossible_move_Black += 1
        if impossible_move_White == 2 or impossible_move_Black == 2:
            return "Game is over. Impossible moves"
        else:
            return "Impossible move"
    # Check ...
    elif map_stecs[int(point) - 1][-1] != checkers:
        if move % 2 == 0:
            impossible_move_White += 1
        else:
            impossible_move_Black += 1
        if impossible_move_White == 2 or impossible_move_Black == 2:
            return "Game is over. Impossible moves"
        else:
            return "Impossible move"
    else:
        return render_template('move.dice.html')  # else: go to /game/move/dice


@app.route('/game/move/dice', methods=['GET'])
def game_move():
    global bar_white, bar_black, map_stecs, white_checkers, black_checkers, dies, move, double, impossible_move_Black, impossible_move_White, action, checkers, point
    print('form:', request.form)
    print('args:', request.args)
    dice_move_str = request.form.get('dice')
    print(dice_move_str)  # player pick what dies he will play.
    dice_move = 0
    if len(dice_move_str) > 1:
        for i in range(0, len(dice_move_str)):
            dice_move += dies[i]
    elif len(dice_move_str) > 4:
        return "There is only two dies"
    else:
        dice_move = dies[int(dice_move_str)]
    if not map_stecs[point - 1 + dice_move]:  # stacks
        map_stecs.pop([point - 1][-1])  #OK
        map_stecs[point - 1 + dice_move].append(str(checkers))
        return "Move is done" + str(len(map_stecs[point - 1 + dice_move]))

    elif map_stecs[point - 1 + dice_move][-1] != checkers:
        if checkers == "Black pies":
            impossible_move_Black += 1  #OK
            return "Impossible move"
        else:
            impossible_move_White += 1
            return "Impossible move"  # come back to start of /game/move
    else:
        map_stecs[point - 1 + dice_move].append(str(checkers))
        map_stecs.pop([point - 1][-1])
        return "Move is done" + str(len(map_stecs[point - 1 + dice_move]))


if __name__ == '__main__':
    app.run(debug=True, port=5005)
