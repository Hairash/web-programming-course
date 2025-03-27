from flask import Flask, request, jsonify

app = Flask('vanya')

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_route():
    print('Request method:', request.method)
    print('Request data:', request.data.decode('utf-8'))
    user_data = request.data.decode('utf-8')
    if request.method == 'GET':
        return jsonify({'a': 1, 'b': 2})
    elif request.method == 'POST':
        return f'Don\'t post here such data: {user_data}'
    return 'Unsupported method'


@app.route('/app', methods=['GET', 'POST'])
def handle_app():
    print('Request args:', request.args)
    args = request.args
    if request.method == 'GET':
        return '''<html>
<head>
    <title>Simple form</title>
</head>

<body>
    <form action="/app" method="post">
        <label for="q">Enter your query:</label>
        <input type="text" id="q" name="q">
        <input type="submit" value="Submit">
    </form>
</body>
</html>
        '''
    elif request.method == 'POST':
        return f'Still no ideas about: {args["q"]}'


app.run(debug=True)
