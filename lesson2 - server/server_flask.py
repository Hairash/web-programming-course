from flask import Flask, request

app = Flask(__name__)


# Handler for the http://127.0.0.1:5000/ URL for our local server
@app.route('/', methods=['GET'])
def hello_world():
    return 'Welcome to the application'


# We define handler for the http://127.0.0.1:5000/app for our local server
@app.route('/app', methods=['GET', 'POST'])  # methods allowed for this URL
def handle_app():
    # request is Flask built-in variable that stores data of current request
    if request.method == 'GET':
        return 'Send POST request with some data'
    elif request.method == 'POST':
        # request.data returns payload of current request as a binary string
        # As we print it, you can see it in console (like b'2')
        print(request.data)
        # Convert request.data to the usual string
        decoded_data = request.data.decode('utf-8')
        return f'You sent data: {decoded_data}'


if __name__ == '__main__':
    app.run(debug=True)
