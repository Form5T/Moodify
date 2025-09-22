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
    },

    "Other Languages": {
        "Korean": "https://open.spotify.com/playlist/37i9dQZF1DWUXxc8Mc6MmJ?si=OmbosJtWQbq5JkALsQcHKw",  
        "Chinese": "https://open.spotify.com/playlist/2QfjrcsUBjP23dL1I01ke3?si=AcLe4A8dQ5-qOQoViVZVZA",  
        "Japanese": "https://open.spotify.com/playlist/0nAJQxdsK0ToL7vLLEWm45?si=QU44Sz-OTrOcS6E3VAaFEg&pi=aBup2cU7QR-fq" 
        }
}

@app.route("/")
def index():
    html = "<h1>User Mood 🎵</h1>"

    for mood, link in playlist_map["English"].items():
        html += f"<h3>{mood.capitalize()}</h3>"
        html += f'<a href="{link}" target="_blank">{mood.capitalize()} Playlist</a><br><br>'

    
    html += "<h2>Other Languages</h2>"
    
    for mood, link in playlist_map["Other Languages"].items():
        html += f"<h3>{mood.capitalize()} Song</h3>"
        html += f'<a href="{link}" target="_blank">{mood.capitalize()} Playlist</a><br><br>'

    return html

if __name__ == "__main__":
    app.run(debug=True)
