from flask import Flask

app = Flask(__name__)

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

@app.route("/")
def index():
    html = "<h1>User Mood 🎵</h1>"

    for mood, link in playlist_map["English"].items():
        html += f"<h3>{mood.capitalize()}</h3>"
        html += f'<a href="{link}" target="_blank">{mood.capitalize()} Playlist</a><br><br>'

    return html

if __name__ == "__main__":
    app.run(debug=True)
