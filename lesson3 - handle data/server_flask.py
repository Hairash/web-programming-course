from flask import Flask, request

app = Flask(__name__)


# http://127.0.0.1:5000/spells endpoint handling different data types
@app.route('/spells', methods=['GET', 'POST', 'DELETE'])
def handle_spells():
    if request.method == 'GET':
        return 'List of spells'
    if request.method == 'POST':
        # request.headers might be utilized like a Python dict
        if request.headers['Content-Type'] == 'application/json':
            obj = request.json
            '''request.json is a real Python dict or list
            Let's say you sent
            {
                "param": "value",
                "coords": {
                    "x": 10,
                    "y": 25
                },
                "list": [
                    1,
                    2,
                    3
                ]
            }
            '''
            print(type(obj))  # <class 'dict'>
            print(obj['param'])  # value
            print(obj['coords']['x'])  # 10
            print(obj['list'][0])  # 1
            return f'JSON detected {obj}'
        elif request.headers['Content-Type'] == 'text/plain':
            # If you send the same data as text, it will be processed as usual string
            s = request.data.decode('utf-8')
            print(type(s))  # <class 'str'>
            print(s[:10])  # {     "par
            return f'Text detected: {s}'
        else:
            # Try different formats
            return 'Unknown format'
    else:
        # Try different methods
        return 'Unknown method'


if __name__ == '__main__':
    app.run(debug=True)
