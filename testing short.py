from flask import Flask, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

CLIENT_ID = "729bcbda83cf484fb1d35d8c9fdd01d4"
CLIENT_SECRET = "ddb4c9c5e7ea436aa4fb6336676e630b" 

# initialise Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

# language，feeling--song
playlist_map = {
    "korean": {
        "happy": "https://open.spotify.com/playlist/3tEiySvyiuoaUV5Uzdd6Tk?si=xMZQiaE7Tk-35Yzdz0bK3Q&pi=4-5Ez1t1TnOcg",
        "chill": "https://open.spotify.com/playlist/yyyyy",
        "sad": "https://open.spotify.com/playlist/zzzzz",
        "love": "https://open.spotify.com/playlist/aaaaa",
        "study": "https://open.spotify.com/playlist/bbbbb",
        "motivational": "https://open.spotify.com/playlist/ccccc",
    },
    "japanese": {
        "happy": "https://open.spotify.com/playlist/ddddd",
        "chill": "...",
        "sad": "...",
        "love": "...",
        "study": "...",
        "motivational": "..."
    },
    "chinese": {
        "happy": "...",
        "chill": "...",
        "sad": "...",
        "love": "...",
        "study": "...",
        "motivational": "..."
    },
    "english": {
        "happy": "...",
        "chill": "...",
        "sad": "...",
        "love": "...",
        "study": "...",
        "motivational": "..."
    }
}

# first page
@app.route("/")
def index():
    return '''
        <h2>🎵 Moodify</h2>
        <form action="/search">
            <input type="text" name="query" placeholder="Search song..." required>
            <input type="submit" value="Search">
        </form>
        <br><br>
        <form action="/recommend">
            <label>Language:</label>
            <select name="language" required>
                <option value="korean">Korean</option>
                <option value="japanese">Japanese</option>
                <option value="chinese">Chinese</option>
                <option value="english">English</option>
            </select>
            <br><br>
            <label>Mood:</label>
            <select name="mood" required>
                <option value="happy">Happy</option>
                <option value="chill">Chill</option>
                <option value="sad">Sad</option>
                <option value="love">Love</option>
                <option value="study">Study</option>
                <option value="motivational">Motivational</option>
            </select>
            <br><br>
            <input type="submit" value="Get Playlist">
        </form>
    '''

# search song
@app.route("/search")
def search():
    query = request.args.get("query", "")
    if not query:
        return "Please enter a search term."

    results = sp.search(q=query, type="track", limit=5)
    output = f"<h2>🔎 Results for '{query}'</h2>"
    for track in results["tracks"]["items"]:
        name = track["name"]
        artist = track["artists"][0]["name"]
        url = track["external_urls"]["spotify"]
        output += f"<p>{name} - {artist} (<a href='{url}' target='_blank'>Open</a>)</p>"
    return output

# recommend feeling
@app.route("/recommend")
def recommend():
    language = request.args.get("language", "")
    mood = request.args.get("mood", "")

    if language not in playlist_map or mood not in playlist_map[language]:
        return "❌ Invalid choice."

    # main recommendation
    main_playlist = playlist_map[language][mood]

    # diff language song recommend
    other_playlists = []
    for lang, moods in playlist_map.items():
        if lang != language:
            other_playlists.append(f"{lang.capitalize()}: <a href='{moods[mood]}' target='_blank'>{moods[mood]}</a>")

    output = f"<h2>🎶 {language.capitalize()} {mood.capitalize()} Playlist</h2>"
    output += f"<p><a href='{main_playlist}' target='_blank'>{main_playlist}</a></p>"
    output += "<h3>🌍 Other languages:</h3>" + "<br>".join(other_playlists)

    return output

if __name__ == "__main__":
    app.run(debug=True)
