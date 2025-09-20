from flask import Flask, request, redirect, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

app = Flask(__name__)
app.secret_key = "super_secret_key"  # random stuff, no need to care

# Spotify API credentials
CLIENT_ID = "b36bdb19978d4feb90e3371816f48ede"
CLIENT_SECRET = "CHANGE HERE"  # <- real key put here
REDIRECT_URI = "http://127.0.0.1:5000/callback"

# Scope: permission we need
SCOPE = "user-read-private"

playlist_map = {
    "English": {
        "happy": "https://open.spotify.com/playlist/0RH319xCjeU8VyTSqCF6M4?si=S9EcINgwTbKCdFlMHgvM7w",
        "chill": "https://open.spotify.com/playlist/2yrMAJe8pqWk3n7l4VYLMk?si=-RvPLBmFQqylQPLTuujNjQ",
        "sad": "https://open.spotify.com/playlist/4bRQf8bwAIVgCb6Lcoursx?si=fQcB_2trR_GkcTY3leSV-A",
        "love": "https://open.spotify.com/playlist/6oNsYDhN95gkENsdFcAwTh?si=Yolvf9P0TB26R7Xv9frCoQ",
        "study": "https://open.spotify.com/playlist/0oPyDVNdgcPFAWmOYSK7O1?si=XiC-GeuHTwm11E-NNCrg6Q",
        "motivational": "https://open.spotify.com/playlist/2fmxVDpboTzLaLAfj5ZaQW?si=aXj9MgsoS3a_s8zEtW_FDg"
    }
}

# Helper to get valid token
def get_token():
    token_info = session.get("token_info", None)
    if not token_info:
        return None

    # Check if token expired
    now = int(time.time())
    is_expired = token_info.get("expires_at") - now < 60

    if is_expired:
        sp_oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE)
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
        session["token_info"] = token_info

    return token_info

# Home page
@app.route("/")
def index():
    token_info = get_token()
    if not token_info:
        return redirect(url_for("login"))

    # Mood playlists
    html = "<h1>Moodify 🎵</h1>"
    html += "<h2>🎶 Mood Playlists</h2>"
    for mood, link in playlist_map["English"].items():
        html += f"<h4>{mood.capitalize()}</h4>"
        html += f'<a href="{link}" target="_blank">{mood.capitalize()} Playlist</a><br><br>'

    # Spotify search form
    html += """
        <h2>🔍 Search Songs</h2>
        <form action="/search">
            <input type="text" name="query" placeholder="Happy, Sad, Chill..." required>
            <input type="submit" value="Search">
        </form>
    """
    return html

# Login with Spotify
@app.route("/login")
def login():
    sp_oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

# Spotify redirect callback
@app.route("/callback")
def callback():
    sp_oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE)
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for("index"))

# Search route
@app.route("/search")
def search():
    token_info = get_token()
    if not token_info:
        return redirect(url_for("login"))

    sp = spotipy.Spotify(auth=token_info["access_token"])
    query = request.args.get("query", "")
    if not query:
        return "Please enter a search term."

    results = sp.search(q=query, limit=10, type="track")
    output = f"<h2>Results for '{query}'</h2>"
    for track in results["tracks"]["items"]:
        name = track["name"]
        artist = track["artists"][0]["name"]
        url = track["external_urls"]["spotify"]
        output += f"<p>{name} - {artist} (<a href='{url}' target='_blank'>Open in Spotify</a>)</p>"
    
    output += "<br><a href='/'>Back to Moodify</a>"
    return output

if __name__ == "__main__":
    app.run(debug=True)