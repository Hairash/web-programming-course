from flask import Flask, request, render_template, jsonify
from werkzeug.utils import redirect

app = Flask('Hospital')

appointments = []


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', appointments=appointments)

@app.route('/appointments', methods=['GET', 'POST'])
def handle_appointments():
    if request.method == 'POST':
        # Handle the form submission
        surname = request.data.decode('utf-8')
        print('Received surname:', surname)
        # Here you would typically save the appointment to a database
        appointments.append(surname)
        # Should return smth to be able to display it on client
        return appointments
    elif request.method == 'GET':
        return appointments



@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

app.run(debug=True, port=5000)
