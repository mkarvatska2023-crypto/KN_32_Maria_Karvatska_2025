from flask import Flask
from jikanpy import Jikan

jikan = Jikan()
app = Flask(__name__)

j = jikan.anime(54595, extension='episodes')

@app.route('/')
def home():
    html = "<h2>Список епізодів</h2><ul>"

    for episode in j["data"]:
        html += f"""
        <li>
            <b>Епізод {episode.get('mal_id')}</b> — {episode.get('title')}
        </li>
        """

    html += "</ul>"
    return html

if __name__ == '__main__':
    app.run(debug=True)