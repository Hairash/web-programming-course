import random
from flask import Flask, request, session, render_template, redirect  # import session to manage user sessions

from flask_sqlalchemy import SQLAlchemy  # import SQLAlchemy to manage the database

app = Flask('authentication')
app.secret_key = 'supersecretkey'  # Required for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database - the file will be created in the same directory
db = SQLAlchemy(app)  # Initialize the database - this will create the database file if it doesn't exist


class User(db.Model):  # Define the User model - related to the table in the database
    id = db.Column(db.Integer, primary_key=True)  # You may specify any columns there
    name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


with app.app_context():  # Create the database and tables
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


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/game')
def game():
    if 'username' in session:
        GameData.players.add(session['username'])  # Add the logged-in user to the players set
        return render_template('game.html')
    return redirect('/')


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

    return {'event': 'Not logged in', 'success': False}

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    print(User.query.all())
    user = User.query.filter_by(name=username).first()
    print(user)
    if user and user.password == password:
        session['username'] = username  # Store the username in the session
        return {'event': 'Login successful', 'success': True}

    return {'event': 'Login failed', 'success': False}


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    print(User.query.all())  # Not needed, just for debugging
    if User.query.filter_by(name=username).first():  # Filter the User table by username
        return 'User already exists'

    new_user = User(name=username, password=password)  # Create a new user instance
    db.session.add(new_user)  # Add the new user to the database session (don't confuse with the browser session)
    db.session.commit()  # Commit the database session to save the new user to the database
    return 'User registered successfully'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
