from flask import Flask, jsonify, request, redirect, session, url_for, send_from_directory, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "super_secret_key"
CORS(app)

# Spotify API credentials
CLIENT_ID = "2ae9791672a54eeca9a0b6d167801ec1"
CLIENT_SECRET = "e0505026734f417093c55a8dcb6ffa19"
REDIRECT_URI = "http://127.0.0.1:5000/callback"

# Scope: we need playlist access
SCOPE = "user-library-read playlist-read-private"

playlist_map = {
    "happy": "0RH319xCjeU8VyTSqCF6M4",
    "chill": "2yrMAJe8pqWk3n7l4VYLMk",
    "sad": "4bRQf8bwAIVgCb6Lcoursx",
    "love": "6oNsYDhN95gkENsdFcAwTh",
    "study": "0oPyDVNdgcPFAWmOYSK7O1",
    "motivational": "2fmxVDpboTzLaLAfj5ZaQW",
    "korean": "37i9dQZF1DWUXxc8Mc6MmJ",   
    "chinese": "2QfjrcsUBjP23dL1I01ke3",    
    "japanese": "0nAJQxdsK0ToL7vLLEWm45"  
}

# Helper to get valid token
def get_token():
    token_info = session.get("token_info", None)
    if not token_info:
        return None

    now = int(time.time())
    is_expired = token_info.get("expires_at") - now < 60

    if is_expired:
        sp_oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE)
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
        session["token_info"] = token_info

    return token_info

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
    token_info = sp_oauth.get_access_token(code, as_dict=True)
    session["token_info"] = token_info
    return redirect(url_for("home"))

# Home page (serve your HTML)
from flask import render_template
@app.route("/")
def home():
    return render_template("HTML.html")
    
# Get all categories
@app.route("/api/categories")
def categories():
    token_info = get_token()
    if not token_info:
        return jsonify({"error": "Not authenticated"}), 401
    return jsonify(sorted(list(playlist_map.keys())))

# Get songs in a category (real Spotify tracks)
@app.route("/api/category/<category>")
def get_category_songs(category):
    token_info = get_token()
    if not token_info:
        return jsonify({"error": "Not authenticated"}), 401

    sp = spotipy.Spotify(auth=token_info["access_token"])
    playlist_id = playlist_map.get(category.lower())
    if not playlist_id:
        return jsonify([])

    results = sp.playlist_tracks(playlist_id, limit=20)
    songs = []
    for item in results["items"]:
        track = item["track"]
        if track is None:  
            continue

        print("TRACK:", track["name"])
        print("ARTISTS:", ", ".join([a["name"] for a in track["artists"]]))
        print("PREVIEW_URL:", track["preview_url"])

        songs.append({
            "id": track["id"],   # 👈 加在这里
            "title": track["name"],
            "artist": ", ".join([a["name"] for a in track["artists"]]),
            "url": track["external_urls"]["spotify"],   # 整首歌
            "preview": track["preview_url"]             # 30 秒试听
        })
    return jsonify(songs)

# Search route
@app.route("/api/search")
def search():
    token_info = get_token()
    if not token_info:
        return jsonify({"error": "Not authenticated"}), 401

    sp = spotipy.Spotify(auth=token_info["access_token"])
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "Please enter a search term."})

    results = sp.search(q=query, limit=10, type="track")
    songs = []
    for track in results["tracks"]["items"]:
        songs.append({
            "id": track["id"],
            "title": track["name"],
            "artist": ", ".join([a["name"] for a in track["artists"]]),
            "url": track["external_urls"]["spotify"],
            "preview": track["preview_url"]
        })
    return jsonify(songs)

@app.route("/api/track/<track_id>")
def get_track(track_id):
    token_info = get_token()
    if not token_info:
        return redirect(url_for("login"))

    sp = spotipy.Spotify(auth=token_info["access_token"])
    track = sp.track(track_id)
    return jsonify(track)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


