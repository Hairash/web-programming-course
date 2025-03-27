import dataclasses
import random

from flask import Flask, jsonify, redirect, request, render_template, url_for

app = Flask(__name__)


@dataclasses.dataclass
class AppData:
    songs = []

'''
Song: {
    'author': 'Flëur',
    'lyrics': 'Я незаметно на дереве в листьях...',
    'chords': 'Cm Gm B Fm ...',
    'solo': 'D# D# D# F F D# D D D# G D ...',
}
'''


@app.route('/', methods=['GET'])
def home():
    return render_template('main.html', songs=AppData.songs)


@app.route('/songs', methods=['GET', 'POST'])
def handle_songs():
    if request.method == 'GET':
        return AppData.songs
    if request.method == 'POST':
        print(request.json)
        AppData.songs.append(request.json)
        print(AppData.songs)
        print(jsonify({'songs': AppData.songs}))
        return jsonify({'songs': AppData.songs})


@app.route('/songs/<int:song_id>', methods=['GET'])
def get_song(song_id):
    song = AppData.songs[song_id]
    return jsonify(song)


if __name__ == '__main__':
    app.run(debug=True)
