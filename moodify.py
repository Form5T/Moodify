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
    return '''
        <h2>Moodify 🎵</h2>
        <p>Search songs by mood or keyword:</p>
        <form action="/search">
            <input type="text" name="query" placeholder="Happy, Sad, Chill..." required>
            <input type="submit" value="Search">
        </form>
    '''

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

    results = sp.search(q=query, limit=5, type="track")
    output = f"<h2>Results for '{query}'</h2>"
    for track in results["tracks"]["items"]:
        name = track["name"]
        artist = track["artists"][0]["name"]
        url = track["external_urls"]["spotify"]
        output += f"<p>{name} - {artist} (<a href='{url}' target='_blank'>Open in Spotify</a>)</p>"
    return output

if __name__ == "__main__":
    app.run(debug=True)