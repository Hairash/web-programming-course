from flask import Flask, redirect, request, render_template, url_for

app = Flask(__name__)

app_data = {'sticks': 21}

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', sticks=app_data['sticks'])


@app.route('/take', methods=['GET', 'POST'])
def handle_app():
    if request.method == 'GET':
        return 'Send your message with the POST request'
    elif request.method == 'POST':
        sticks = int(request.form.get('sticks'))
        print(sticks)
        app_data['sticks'] -= sticks
        return redirect(url_for('home'))
        # return f'You took {sticks} sticks'


if __name__ == '__main__':
    app.run(debug=True)
