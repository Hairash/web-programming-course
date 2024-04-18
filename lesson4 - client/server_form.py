import random

from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

'''API:
GET /tasks - return list of tasks
GET /next_task - return next task
POST /tasks - add task to the server
POST /answer {'task': '<task_id>'} - send answer to the server, return True/False
'''

tasks = []
current_task_idx = -1


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', tasks=tasks)  # return html with parameters


@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'GET':
        return tasks
    if request.method == 'POST':
        print(request.form)  # dict of values sent by html form
        tasks.append(request.form['task'])  # the answer might be stored as well
        # redirect to another page in this case to url_for(home) == '/'
        return redirect(url_for('home'))


@app.route('/next_task', methods=['GET'])
def get_next_task():
    global current_task_idx
    current_task_idx += 1
    current_task = tasks[current_task_idx]
    return current_task


@app.route('/answer', methods=['POST'])
def handle_answer():
    global current_task_idx
    answer = request.data.decode('utf-8')
    # There should be some logic, checking the answer
    return str(bool(random.randint(0, 1)))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
