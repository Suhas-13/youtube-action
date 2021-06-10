from youtube_dl import YoutubeDL
from flask import Flask, render_template, request, url_for, flash, redirect, Response, session, jsonify
app = Flask(__name__)

host = '0.0.0.0'
port = 5387 
youtube_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': False,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'cachedir': False
}

output_from_query = {
    "session": {
        "id": "",
        "params": {}
    },
    "scene": {
        "name": "",
        "slots": {},
        "next": {
            "name": ""
        }
    },
}

ytdl = YoutubeDL(youtube_options)


def create_query_response(params, session_id, current_scene, next_scene):
    output = output_from_query.copy()
    output['session']['params'] = params
    output['session']['id'] = session_id
    output['scene']['name'] = current_scene
    output['scene']['next']['name'] = next_scene
    return jsonify(output)


def play(params, session):
    if params:
        song_name = params.get("song_name")
        if song_name:
            song_name_parsed = song_name.get("resolved")
    if song_name_parsed:
        song_data = get_query_results(song_name_parsed)
        song_url = song_data.get("song_url")
        channel_name = song_data.get("channel_name")
        actual_song_name = song_data.get("song_name")
        if song_url and actual_song_name and channel_name:
            return create_query_response({"found": True, "song_name": actual_song_name, "song_url": song_url, "channel_name": channel_name}, session.get("id"), "fill_play", "start_play")
    return create_query_response({"found": False, "song_name": "", "song_url": "", "channel_name": ""}, session.get("id"), "fill_play", "start_play")

@app.route("/api", methods=['POST'])
def api():
    json_data = request.get_json(force=True)
    handler = json_data.get("handler")
    if handler:
        if handler.get("name") == "play":
            intent = json_data.get("intent")
            if intent:
                params = intent.get("params")
            session = json_data.get("session")
            response = play(params, session)
            return response
    return {"msg": "Invalid parameter(s)"}, 422


def get_query_results(query):
    if not query:
        return {}
    data = ytdl.extract_info(f"ytsearch:{query}", download=False)
    search_results = data['entries']
    if not search_results:
        return {}
    result = search_results[0]
    song_name = result['title']
    channel_name = result['uploader']
    for format_ in result['formats']:
        if format_['ext'] == 'm4a':
            m4a_url = format_['url']
            return {"song_name": song_name, "channel_name": channel_name, "song_url": m4a_url}
    return {}


if __name__ == "__main__":
    app.run(host = host, port=port, debug=False)

