import random

from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Setup connection to the database (DB)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://teacher:9876@localhost:5432/quiz_app'
# Variable, responsible for DB connection
db = SQLAlchemy(app)


# The model that represents data in the 'tasks' table
# 3 columns (id, question, answer)
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(100), nullable=False)


# Create all the table on app run (if they don't exist)
with app.app_context():
    db.create_all()


app_data = {
    'tasks': [],
    'current_task_idx': -1,
}


@app.route('/', methods=['GET'])
def home():
    # Get all the tasks from the DB
    res = db.session.query(Task).all()
    # Then process them as Task objects
    # (e.g. task.question - is the string, that stores text of the question)
    return render_template('ajax.html', tasks=[task.question for task in res])


@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'GET':
        res = db.session.query(Task).all()
        print(res)
        return res
    if request.method == 'POST':
        print(request.json)
        # Create new Task object (id field is created automatically)
        new_task = Task(
            question=request.json['task'],
            answer=request.json['answer'],
        )
        # Add new task to the database
        db.session.add(new_task)
        # Apply changes (send all the commands to the DB)
        db.session.commit()

        res = db.session.query(Task).all()
        print(type(res))  # list
        print(res)

        print([task.question for task in res])  # list of question only
        return jsonify({'tasks': [task.question for task in res]})


@app.route('/next_task', methods=['GET'])
def get_next_task():
    global current_task_idx
    current_task_idx += 1
    current_task = app_data['tasks'][current_task_idx]
    return current_task


@app.route('/answer', methods=['POST'])
def handle_answer():
    global current_task_idx
    answer = request.data.decode('utf-8')
    # There should be some logic, checking the answer
    return str(bool(random.randint(0, 1)))


if __name__ == '__main__':
    app.run(debug=True)
