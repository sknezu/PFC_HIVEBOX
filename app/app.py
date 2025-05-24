from flask import Flask, jsonify, Response, render_template
import requests
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jsonpath_ng.ext import parse
from dateutil import parser as createdAt_parser
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import threading
import time

# Load environment variables
load_dotenv()
SENSEBOX_IDS = os.getenv('SENSEBOX_IDS', '').split(',')
SENSEBOX_NAMES = os.getenv('SENSEBOX_NAMES', '').split(',')
API_VERSION = os.getenv('API_VERSION', '0.0.0')

# Create a mapping between IDs and names
SENSEBOX_MAP = dict(zip(SENSEBOX_IDS, SENSEBOX_NAMES))

# Prometheus gauge: label by box_id and name
temperature_gauge = Gauge('sensor_temperature_celsius', 'Sensor temperature in °C', ['box_id', 'name'])

@dataclass
class TemperatureInfo:
    createdAt: str
    value: float

    @classmethod
    def from_dict(cls, data: dict) -> "TemperatureInfo":
        jsonpath_expression = parse('$.sensors[?(@.unit=="°C")].lastMeasurement')
        created_at = ""
        value = 0.0
        for match in jsonpath_expression.find(data):
            try:
                created_at = match.value.get('createdAt', '')
                if created_at:
                    created_at_fmt = createdAt_parser.isoparse(created_at)
                    if created_at_fmt > (datetime.now(timezone.utc) - timedelta(hours=1)):
                        value = float(match.value.get('value', 0.0))
                        break
            except Exception as e:
                print(f"Error parsing temperature data: {e}")
        return cls(createdAt=created_at, value=value)

def status_assess(temp):
    if temp <= 10.0:
        return '[ALERT] Too Cold, Bees are freezing!'
    elif temp <= 36.0:
        return 'Good, Bees are happy :)'
    else:
        return '[ALERT] Too Hot, Bees are cooking!'

def update_temperature_metrics():
    for SENSEBOX_ID in SENSEBOX_IDS:
        try:
            response = requests.get(
                f"https://api.opensensemap.org/boxes/{SENSEBOX_ID}?format=json",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            temperature_info = TemperatureInfo.from_dict(data)
            sensor_name = SENSEBOX_MAP.get(SENSEBOX_ID, "Unnamed")
            is_valid = temperature_info.createdAt != ""
            temp_value = temperature_info.value if is_valid else 0.0

            # Update Prometheus gauge
            temperature_gauge.labels(box_id=SENSEBOX_ID, name=sensor_name).set(temp_value)

        except requests.RequestException as e:
            # Optionally reset gauge or set to 0 on error
            temperature_gauge.labels(box_id=SENSEBOX_ID, name=SENSEBOX_MAP.get(SENSEBOX_ID, "Unnamed")).set(0.0)

def update_metrics_periodically(interval=60):
    while True:
        update_temperature_metrics()
        time.sleep(interval)

def create_app(testing=False):
    app = Flask(__name__)
    metrics = PrometheusMetrics(app)
    metrics.info('app_info', 'Application info', version=API_VERSION)

    # Start background thread to update metrics every 60 seconds
    thread = threading.Thread(target=update_metrics_periodically, args=(60,), daemon=True)
    thread.start()

    @app.route('/')
    def index():
        box_results = []
        valid_readings = []
        checked_at = datetime.now(timezone.utc).isoformat()

        for SENSEBOX_ID in SENSEBOX_IDS:
            try:
                response = requests.get(
                    f"https://api.opensensemap.org/boxes/{SENSEBOX_ID}?format=json",
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()

                temperature_info = TemperatureInfo.from_dict(data)
                sensor_name = SENSEBOX_MAP.get(SENSEBOX_ID, "Unnamed")

                is_valid = temperature_info.createdAt != ""
                temp_value = temperature_info.value if is_valid else 0.0
                status = status_assess(temp_value) if is_valid else "No valid reading"

                if is_valid:
                    valid_readings.append(temp_value)

                box_results.append({
                    "name": sensor_name,
                    "box_id": SENSEBOX_ID,
                    "temperature": temp_value,
                    "status": status,
                    "checked_at": checked_at
                })

            except requests.RequestException as e:
                box_results.append({
                    "name": SENSEBOX_MAP.get(SENSEBOX_ID, "Unnamed"),
                    "box_id": SENSEBOX_ID,
                    "temperature": None,
                    "status": "API request failed",
                    "checked_at": checked_at,
                    "error": str(e)
                })

        avg_temp = sum(valid_readings) / len(valid_readings) if valid_readings else None

        return render_template(
            "index.html",
            version=API_VERSION,
            average_temperature=avg_temp,
            readings=box_results
        )

    @app.route('/version')
    def get_version():
        return jsonify({"version": API_VERSION})

    @app.route('/metrics')
    def metrics_route():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
