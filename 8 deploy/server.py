import os  # import os to access environment variables
import random
from flask import Flask, request, session, render_template, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask('sticks_game')
app.secret_key = os.getenv('SECRET_KEY')  # Get the secret key from environment variables
# To set environment variables locally you can use a command like this:
# `export SECRET_KEY=yourkey`
# To set it in Render you can go to the settings of your service and add it there

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()


# Game states - may be done as strings, but this is more clear
class GAME_STATES:
    LOBBY = 'lobby'
    PLAYING = 'playing'


# Way to store game data. You can use a dict instead or even global variables.
# Sometimes it makes sense to store game data in the database
class GameData:
    state = GAME_STATES.LOBBY
    players = set()
    sticks = 0
    actions = set()
    players_queue = []
    current_player_idx = 0


#### Pages
@app.route('/')
def index():
    return render_template('login.html')


@app.route('/game')
def game():
    if 'username' in session:
        # TODO: Don't add players when the game is already started
        GameData.players.add(session['username'])
        return render_template('game.html')
    return redirect('/')


#### API calls
@app.route('/game_data', methods=['GET'])
def game_data():
    if 'username' in session:
        return {
            'state': GameData.state,
            'players': list(GameData.players),
            'sticks': GameData.sticks,
            'actions': list(GameData.actions),
            'current_player': GameData.players_queue[GameData.current_player_idx] if GameData.players_queue else None,
        }
    return {'state': GAME_STATES.LOBBY, 'players': []}


@app.route('/current_user', methods=['GET'])
def current_user():
    if 'username' in session:
        return {'name': session['username']}
    return {'name': None}


@app.route('/start_game', methods=['POST'])
def start_game():
    if 'username' in session and GameData.state == GAME_STATES.LOBBY:
        GameData.state = GAME_STATES.PLAYING
        GameData.sticks = random.randint(10, 100)
        # TODO: Check actions are different
        GameData.actions = {random.randint(2, 10) for _ in range(2)}
        GameData.actions.add(1)
        GameData.players_queue = list(GameData.players)  # TODO: Shuffle

        return {'event': 'Game started', 'success': True}
    return {'event': 'Game not started', 'success': False}


@app.route('/action', methods=['POST'])
def action():
    if (
            'username' in session and GameData.state == GAME_STATES.PLAYING and
            GameData.players_queue[GameData.current_player_idx] == session['username']
    ):
        action = int(request.json.get('action'))
        print(action)
        if action in GameData.actions and GameData.sticks - action >= 0:
            GameData.sticks -= action
            GameData.current_player_idx = (GameData.current_player_idx + 1) % len(GameData.players_queue)
            # TODO: Add winning condition and start new game

    return {'event': 'Not logged in', 'success': False}


#### Authentication
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(name=username).first()
    if user and user.password == password:
        session['username'] = username
        return {'event': 'Login successful', 'success': True}

    return {'event': 'Login failed', 'success': False}


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    print(User.query.all())  # Not needed, just for debugging
    if User.query.filter_by(name=username).first():
        return 'User already exists'

    new_user = User(name=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return 'User registered successfully'


@app.route('/logout', methods=['POST'])
def logout():
    # TODO: Add logout functionality
    session.pop('username', None)


# This is very important to run the app with unicorn on Render
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
