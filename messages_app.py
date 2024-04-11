from flask import Flask, request

app = Flask(__name__)

messages = []


# Handler for the http://google.com/ URL for our local server
@app.route('/', methods=['GET'])
def hello_world():
    # return list of messages as HTML
    messages2 = ''
    for i in range(len(messages)):
        messages2 += messages[i] + '<br>'
    return messages2


@app.route('/messages/', methods=['POST'])
def post_message():
    # store message
    message1 = request.data.decode('utf-8')
    messages.append(message1)
    return 'Message sent'


# We define handler for the http://127.0.0.1:5000/app for our local server
@app.route('/app/', methods=['GET', 'POST'])  # methods allowed for this URL
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
        return f'Hello world: {decoded_data}'


@app.route('/spells', methods=['GET', 'POST', 'DELETE'])  # methods allowed for this URL
def handle_spells():
    if request.method == 'GET':
        return 'List of spells'
    if request.method == 'POST':

        if request.headers['Content-Type'] == 'application/json':
            obj = request.json
            print(type(obj))
            print(obj['param'])
            print(obj['coords']['x'])
            return f'JSON detected {obj}'
        elif request.headers['Content-Type'] == 'text/plain':
            s = request.data.decode('utf-8')
            print(type(s))
            print(s[:10])
            return f'Text detected: {s}'
        else:
            return 'Unknown format'
    else:
        return 'Unknown method'


if __name__ == '__main__':
    app.run(debug=True)
