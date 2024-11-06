from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock databases
songs = {}
playlists = {}

@app.route('/songs', methods=['POST'])
def create_song():
    data = request.json
    song_id = data.get('id')
    songs[song_id] = data
    return jsonify({'message': 'Song created', 'song': data}), 201

@app.route('/songs/<song_id>', methods=['PUT'])
def update_song(song_id):
    data = request.json
    if song_id in songs:
        songs[song_id].update(data)
        return jsonify({'message': 'Song updated', 'song': songs[song_id]})
    return jsonify({'error': 'Song not found'}), 404

@app.route('/songs/<song_id>', methods=['DELETE'])
def delete_song(song_id):
    if song_id in songs:
        del songs[song_id]
        return jsonify({'message': 'Song deleted'})
    return jsonify({'error': 'Song not found'}), 404

@app.route('/songs/<song_id>', methods=['GET'])
def get_song(song_id):
    if song_id in songs:
        return jsonify({'song': songs[song_id]})
    return jsonify({'error': 'Song not found'}), 404

@app.route('/playlists', methods=['POST'])
def create_playlist():
    data = request.json
    playlist_name = data.get('name')
    playlists[playlist_name] = []
    return jsonify({'message': 'Playlist created', 'playlist': playlist_name}), 201

@app.route('/playlists/<playlist_name>', methods=['GET'])
def get_playlist(playlist_name):
    if playlist_name in playlists:
        return jsonify({'playlist': playlists[playlist_name]})
    return jsonify({'error': 'Playlist not found'}), 404

@app.route('/playlists/<playlist_name>', methods=['PUT'])
def update_playlist(playlist_name):
    data = request.json
    if playlist_name in playlists:
        playlists[playlist_name] = data.get('songs', playlists[playlist_name])
        return jsonify({'message': 'Playlist updated', 'playlist': playlists[playlist_name]})
    return jsonify({'error': 'Playlist not found'}), 404

@app.route('/playlists/<playlist_name>', methods=['DELETE'])
def delete_playlist(playlist_name):
    if playlist_name in playlists:
        del playlists[playlist_name]
        return jsonify({'message': 'Playlist deleted'})
    return jsonify({'error': 'Playlist not found'}), 404

@app.route('/playlists/<playlist_name>/add', methods=['POST'])
def add_song_to_playlist(playlist_name):
    data = request.json
    song_id = data.get('song_id')
    if playlist_name in playlists and song_id in songs:
        playlists[playlist_name].append(song_id)
        return jsonify({'message': 'Song added to playlist'})
    return jsonify({'error': 'Playlist or song not found'}), 404

@app.route('/playlists/<playlist_name>/remove', methods=['POST'])
def remove_song_from_playlist(playlist_name):
    data = request.json
    song_id = data.get('song_id')
    if playlist_name in playlists and song_id in playlists[playlist_name]:
        playlists[playlist_name].remove(song_id)
        return jsonify({'message': 'Song removed from playlist'})
    return jsonify({'error': 'Playlist or song not found'}), 404

@app.route('/playlists/<playlist_name>/sort', methods=['POST'])
def sort_playlist(playlist_name):
    data = request.json
    sort_key = data.get('sort_by', 'name')
    if playlist_name in playlists:
        sorted_songs = sorted(playlists[playlist_name], key=lambda song_id: songs[song_id][sort_key])
        playlists[playlist_name] = sorted_songs
        return jsonify({'message': 'Playlist sorted', 'playlist': playlists[playlist_name]})
    return jsonify({'error': 'Playlist not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)


# 4. Key Features on Data Structures
# Stacks and Queues: These can be useful if you want to manage playlist in a way that songs are added or removed from the ends. Example, a queue can manage a "play next" feature.
# Linked Lists: They could be useful for efficienly inserting and deleting songs from the middle of a playlist, but python list structure, which is a dynamic array, often suffices for typical use cases.
# Efficient Search/ Sort Alogorithms: For searching, if you have very large datasets, consider using a binary search on sorted data. For sorting, leveraging Timsort (Python's built-in sort) is typically sufficient. Make sure to test each endpoint and function for reliability and efficiency.
