from flask import Flask, jsonify
from flask_cors import CORS
import requests
from calculations import compute_weighted_average

app = Flask(__name__)
CORS(app)

BASE_URL = "https://api.zeroc.green/v1/"

@app.route("/api/stations", methods=["GET"])
def get_stations():
    """Proxy verso l’API upstream per ottenere la lista delle stazioni"""
    try:
        r = requests.get(f"{BASE_URL}stations/", timeout=10)
        r.raise_for_status()
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 502

@app.route("/api/stations/<station_id>", methods=["GET"])
def get_station_detail(station_id):
    """Proxy verso l’API upstream per ottenere il dettaglio di una stazione
    + aggiunge la media ponderata degli ultimi 7 giorni per ogni metrica
    """
    try:
        r = requests.get(f"{BASE_URL}stations/{station_id}", timeout=10)
        r.raise_for_status()
        data = r.json()

        # ciclo su tutte le metriche disponibili
        metrics = data.get("metrics") or []

        if isinstance(metrics, dict):
            items = metrics.items()
        else:
            items = ((metric.get("name", str(index)), metric) for index, metric in enumerate(metrics))

        for _, metric_data in items:
            days = metric_data.get("daily") or metric_data.get("data_points", [])
            metric_data["daily"] = days
            metric_data["weighted_average_last7"] = compute_weighted_average(days)

        data["metrics"] = metrics
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 502

if __name__ == "__main__":
    app.run(debug=True, port=5000)
