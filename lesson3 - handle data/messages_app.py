from flask import Flask, request

app = Flask(__name__)

messages = []


# Main page for our app, we may see it in browser by http://127.0.0.1:5000 URL
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


if __name__ == '__main__':
    app.run(debug=True)
