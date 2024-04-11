from flask import Flask, request

app = Flask(__name__)

messages = []


@app.route('/', methods=['GET'])
def main_page():
    message_strs = [f'{m["author"]}: {m["message"]}' for m in messages]
    return '<br>'.join(message_strs)


@app.route('/messages', methods=['GET', 'POST'])  # methods allowed for this URL
def handle_app():
    if request.method == 'GET':
        return 'Send your message with the POST request'
    elif request.method == 'POST':
        # decoded_data = request.data.decode('utf-8')
        # request.json['author']
        messages.append(request.json)
        return f'You sent data: {request.json}'


if __name__ == '__main__':
    app.run(debug=True)
