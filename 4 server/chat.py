from flask import Flask, request

app = Flask('Sasha')

messages = []


@app.route('/messages', methods=['POST'])
def send_message():
    # Add checks!
    messages.append((request.json['name'], request.json['text']))
    return 'Message sent'

@app.route('/messages', methods=['GET'])
def get_messages():
    message_list = ''
    for name, text in messages:
        message_list += '<br>' + name + ': ' + text
    return message_list


app.run(debug=True, port=5001)

