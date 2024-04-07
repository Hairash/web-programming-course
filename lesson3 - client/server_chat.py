from flask import Flask, request

app = Flask(__name__)

messages = []


@app.route('/', methods=['GET'])
def hello_world():
    return f'All the messages: {messages}'


@app.route('/messages', methods=['GET', 'POST'])  # methods allowed for this URL
def handle_app():
    if request.method == 'GET':
        return 'Send POST request with some data'
    elif request.method == 'POST':
        decoded_data = request.data.decode('utf-8')
        messages.append(decoded_data)
        return f'You sent data: {decoded_data}'


if __name__ == '__main__':
    app.run(debug=True)
