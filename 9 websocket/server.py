import os
import random
from flask import Flask, request, session, render_template, redirect
# Don't forget to add flask-socketio to your requirements.txt
from flask_socketio import SocketIO, emit  # import SocketIO for real-time communication

from flask_sqlalchemy import SQLAlchemy

app = Flask('sticks_game')
app.secret_key = os.getenv('SECRET_KEY', 'topsecret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Initialize SocketIO with CORS support


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()


class GAME_STATES:
    LOBBY = 'lobby'
    PLAYING = 'playing'


class GameData:
    state = GAME_STATES.LOBBY
    players = set()
    sticks = 0
    actions = set()
    players_queue = []
    current_player_idx = 0


#### SocketIO events
@socketio.on('connect')  # Handle client connection
def handle_connect():
    if 'username' in session:
        print(f'Client connected {request.sid}')
        GameData.players.add(session['username'])
        # socketio.emit - sends a message to all connected clients
        # emit - sends a message to the client that triggered the event (like response to a request)
        socketio.emit('players', list(GameData.players))  # Send the list of players to all clients
        emit('current_user', session['username'])  # Send the current user to the client


@socketio.on('disconnect')
def handle_disconnect():
    if 'username' in session:
        GameData.players.discard(session['username'])
        socketio.emit('players', list(GameData.players))  # Update the list of players for all clients
        print(f'Client disconnected {request.sid}')


@socketio.on('start_game')
def start_game():
    if 'username' in session and GameData.state == GAME_STATES.LOBBY:
        GameData.state = GAME_STATES.PLAYING
        GameData.sticks = random.randint(10, 100)
        # TODO: Check actions are different
        # TODO: Check actions have different remainders divided by players' number
        GameData.actions = {random.randint(2, 10) for _ in range(2)}
        GameData.actions.add(1)
        GameData.players_queue = list(GameData.players)  # TODO: Shuffle
        socketio.emit('game_started', {  # Notify all clients that the game has started
            'actions': list(GameData.actions),
            'players': GameData.players_queue,
        })
        socketio.emit('game_state', {  # Send the initial game state to all clients
            'state': GameData.state,
            'sticks': GameData.sticks,
            'current_player': GameData.players_queue[GameData.current_player_idx],
        })


@socketio.on('action')
def handle_action(data):
    if (
            'username' in session and GameData.state == GAME_STATES.PLAYING and
            GameData.players_queue[GameData.current_player_idx] == session['username']
    ):
        action = int(data)
        print(action)
        if action in GameData.actions and GameData.sticks - action >= 0:
            GameData.sticks -= action
            GameData.current_player_idx = (GameData.current_player_idx + 1) % len(GameData.players_queue)
            socketio.emit('game_state', {  # Update the game state for all clients
                'sticks': GameData.sticks,
                'current_player': GameData.players_queue[GameData.current_player_idx],
            })
        else:
            # Invalid action, notify the client
            socketio.emit('invalid_action', {'error': 'Invalid action'})
    else:
        socketio.emit('invalid_action', {'error': 'Game not started or invalid player'})


#### Pages
@app.route('/')
def index():
    return render_template('login.html')


@app.route('/game')
def game():
    if 'username' in session:
        return render_template('game.html')
    return redirect('/')


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
