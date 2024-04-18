import random

from flask import Flask, jsonify, redirect, request, render_template, url_for

app = Flask(__name__)

# The way to store all the data inside one object
app_data = {
    'tasks': [],
    'current_task_idx': -1,
}


@app.route('/', methods=['GET'])
def home():
    return render_template('ajax.html', tasks=app_data['tasks'])


@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'GET':
        return app_data['tasks']
    if request.method == 'POST':
        # Here we receive JSON
        print(request.json)  # dict of values sent by the fetch() function
        app_data['tasks'].append(request.json['task'])  # the answer might be stored as well
        # return all the data to immediately output in on the page
        print(app_data['tasks'])
        print(jsonify({'tasks': app_data['tasks']}))
        return jsonify({'tasks': app_data['tasks']})


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
