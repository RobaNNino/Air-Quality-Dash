from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

BASE_URL = "https://api.zeroc.green/v1"

@app.route("/api/stations", methods=["GET"])
def get_stations():
    """Proxy verso l’API upstream per ottenere la lista delle stazioni"""
    try:
        r = requests.get(f"{BASE_URL}/stations", timeout=10)
        r.raise_for_status()
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 502


if __name__ == "__main__":
    app.run(debug=True, port=5000)
