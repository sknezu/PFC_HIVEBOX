from flask import Flask, jsonify
import requests
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jsonpath_ng.ext import parse
from dateutil import parser as createdAt_parser
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge

# Load environment variables
load_dotenv()
SENSEBOX_IDS = os.getenv('SENSEBOX_IDS', '').split(',')
SENSEBOX_NAMES = os.getenv('SENSEBOX_NAMES', '').split(',')
API_VERSION = os.getenv('API_VERSION', '0.0.0')

# Create a mapping between SENSEBOX_IDs and their names
SENSEBOX_MAP = dict(zip(SENSEBOX_IDS, SENSEBOX_NAMES))

# Prometheus metric
temperature_gauge = Gauge('sensor_temperature_celsius', 'Sensor temperature in °C', ['box_id', 'name'])

@dataclass
class TemperatureInfo:
    createdAt: str
    valid: bool
    value: float

    @classmethod
    def from_dict(cls, data: dict) -> "TemperatureInfo":
        jsonpath_expression = parse('$.sensors[?(@.unit=="°C")].lastMeasurement')
        valid = False
        value = 0.0
        created_at = ""
        for match in jsonpath_expression.find(data):
            try:
                created_at = match.value.get('createdAt', '')
                if created_at:
                    created_at_fmt = createdAt_parser.isoparse(created_at)
                    if created_at_fmt > (datetime.now(timezone.utc) - timedelta(hours=1)):
                        value = float(match.value.get('value', 0.0))  # Default to 0 if no value is found
                        valid = True
                        break
            except Exception as e:
                print(f"Error parsing temperature data: {e}")
        return cls(createdAt=created_at, value=value, valid=valid)

def status_assess(avg_temp):
    if avg_temp <= 10.0:
        return '[ALERT]Too Cold, Bees are freezing!'
    elif avg_temp > 10.0 and avg_temp <= 36.0:
        return 'Good, Bees are happy :)'
    else:
        return '[ALERT]Too Hot, Bees are cooking!'

def create_app(testing=False):
    app = Flask(__name__)
    metrics = PrometheusMetrics(app)

    @app.route('/temperature', methods=['GET'])
    def get_readings():
        box_results = []
        valid_readings = []
        checked_at = datetime.now(timezone.utc).isoformat()

        try:
            for SENSEBOX_ID in SENSEBOX_IDS:
                api_endpoint = f"https://api.opensensemap.org/boxes/{SENSEBOX_ID}?format=json"
                response = requests.get(api_endpoint, timeout=10)
                response.raise_for_status()
                data = response.json()

                temperature_info = TemperatureInfo.from_dict(data)
                sensor_name = SENSEBOX_MAP.get(SENSEBOX_ID, "Unnamed")
                sensor_status = status_assess(temperature_info.value) if temperature_info.valid else "No valid reading"

                if temperature_info.valid:
                    valid_readings.append(temperature_info.value)

                # Update Prometheus gauge
                temperature_gauge.labels(box_id=SENSEBOX_ID, name=sensor_name).set(temperature_info.value)

                box_results.append({
                    "name": SENSEBOX_MAP.get(SENSEBOX_ID, "Unnamed"),
                    "box_id": SENSEBOX_ID,
                    "temperature": temperature_info.value,
                    "status": sensor_status,
                    "checked_at": checked_at
                })

           # Compute average
            if valid_readings:
                avg_temp = sum(valid_readings) / len(valid_readings)
            else:
                avg_temp = None
                status = "No valid readings to assess status"

            return jsonify({
                "average_temperature": avg_temp,
                "readings": box_results
            }), 200

        except requests.RequestException as e:
            return jsonify({
                "ERROR": "Failed to fetch data from external API",
                "details": str(e)
            }), 500
         
    @app.route('/version', methods=['GET'])
    def get_version():
        version = os.getenv("API_VERSION", "0.0.0")  # Default value if not found
        return jsonify({"version": version})

    @app.route('/')
    def index():
        return (
            "<h1>Welcome to this python app by Miriam C. Palanca</h1>"
            "<p>You can check the version of the app with /version and /temperature to check the hivebox status.</p>"
        )

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
