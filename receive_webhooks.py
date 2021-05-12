from flask import Flask, request, Response
from flask_cors import CORS
import json
import logging
import text_to_speech

app = Flask(__name__)
CORS(app)

@app.route('/webhook', methods=['POST'])
def respond():
    try:
        url = request.json['url']
        text_to_speech.download_clip(url, "titre", )
        return Response(status=200)
    except json.decoder.JSONDecodeError:
        logging.error("pas d'url de téléchargement trouvée")
        return Response(status=400)
