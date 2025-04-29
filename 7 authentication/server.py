from flask import Flask, request, session, render_template  # import session to manage user sessions

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


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(name=username).first()
    if user and user.password == password:
        # token = '123456' - not needed if using session
        # print(f'Login successful, token: {token}')
        session['username'] = username  # Store the username in the session
        return {'event': 'Login successful', 'success': True}

    return 'Login failed'


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


@app.route('/action', methods=['GET'])
def action():
    # Check if the user is logged in
    # token = request.args.get('token')
    # if token == '123456':
    if 'username' in session:  # Check the session. Session is automatically stored in browser cookies
        return render_template('action.html', user_data=session['username'])

    return 'Not authenticated'


app.run(port=5001)
