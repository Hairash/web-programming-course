import time

from flask import Flask

app = Flask(__name__)


@app.route('/sync', methods=['GET'])
def sync_server_check():
    time.sleep(10)
    return 'Sync server is up and running'

app.run(debug=True, threaded=True)
