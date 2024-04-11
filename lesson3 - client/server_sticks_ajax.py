from flask import Flask, jsonify, redirect, request, render_template, url_for

app = Flask(__name__)

app_data = {'sticks': 21}

@app.route('/', methods=['GET'])
def home():
    return render_template('ajax.html', sticks=app_data['sticks'])


@app.route('/take', methods=['GET', 'POST'])
def handle_app():
    if request.method == 'GET':
        return 'Send your message with the POST request'
    elif request.method == 'POST':
        print(request.json)
        sticks = int(request.json['sticks'])
        print(sticks)
        app_data['sticks'] -= sticks
        return jsonify({ 'table': app_data['sticks'] })
        # return f'You took {sticks} sticks'


if __name__ == '__main__':
    app.run(debug=True)
