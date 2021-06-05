from youtube_dl import YoutubeDL
from flask import Flask, render_template, request, url_for, flash, redirect, Response, session, jsonify
app = Flask(__name__)

youtube_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': False,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto'
}
ytdl = YoutubeDL(youtube_options)
@app.route("/api", methods=['POST'])
def api():
    
    json_data = request.get_json(force=True)
    print(json_data)
    song_name = json_data["intent"]["params"]["song_name"]["resolved"]
    song_url = get_query_results(song_name)
    
    return jsonify({
            "session": {
            "id": json_data['session']['id'],
            "params": {"song_name":song_name, "song_url":song_url}
            },
            "scene": {
            "name": "play",
            "slots": {},
            "next": {
            "name": "actual"
            }
        },
    })

def get_query_results(query):
    if not query:
        return ""
    data = ytdl.extract_info(f"ytsearch:{query}", download=False)
    search_results = data['entries']

    if not search_results:
        return ""

    result = search_results[0]
    song_name = result['title']
    channel_name = result['uploader']

    for format_ in result['formats']:
        if format_['ext'] == 'm4a':
            mp3_url = format_['url']
            return mp3_url

    return ""



if __name__ == "__main__":
    app.run(port = 5387, debug=True)
