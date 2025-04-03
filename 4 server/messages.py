from flask import Flask, request

app = Flask('Dasha')


@app.route('/')
def any_name():
    # string
    name = 'Artem'
    return f'Hello {name}!'


@app.route('/html')
def return_html():
    # html
    s = '<html><head><title>Simple form</title></head><body>Hello one-string world!</body>'
    print(type(s))
    return s


@app.route('/json')
def return_json():
    # json
    return [{'a': 1, 'b': '2'}, 'hello', 3]


@app.route('/bin')
def return_binary():
    # Hometask
    return request.data


@app.route('/data', methods=['POST'])
def get_data():
    if request.content_type == 'text/plain':
        print(f'Text: {request.data}')
        return request.data

    elif request.content_type == 'text/html':
        print(f'HTML: {request.data}')
        return request.data

    elif request.content_type == 'application/json':
        print(f'JSON: {request.json}')
        return request.json


app.run(debug=True, port=5001)
