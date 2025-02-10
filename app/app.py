from flask import Flask, jsonify
import requests
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jsonpath_ng.ext import parse
from dateutil import parser as createdAt_parser

# Load environment variables
load_dotenv()
SENSEBOX_IDS = os.getenv('SENSEBOX_IDS', '').split(',')
API_VERSION = os.getenv('API_VERSION', '0.0.0')

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
                        valid = True
                        value = float(match.value.get('value', 0.0))  # Default to 0 if no value is found
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

    @app.route('/temperature', methods=['GET'])
    def get_readings():
        results = []
        try:
            for SENSEBOX_ID in SENSEBOX_IDS:
                api_endpoint = f"https://api.opensensemap.org/boxes/{SENSEBOX_ID}?format=json"
                response = requests.get(api_endpoint, timeout=100)
                response.raise_for_status()
                data = response.json()
                temperature_info = TemperatureInfo.from_dict(data)
                if temperature_info.valid:
                    results.append(temperature_info.value)

            if results:
                avg_temp = sum(results) / len(results)
                return jsonify({"Average temperature": f"{avg_temp}", "Status": f"{status_assess(avg_temp)}"}), 200
            else:
                return jsonify({"ERROR": "No valid temperature readings found"}), 500
        except requests.RequestException as e:
            return jsonify({"ERROR": "Failed to fetch data from external API", "details": str(e)}), 500

    @app.route('/version', methods=['GET'])
    def get_version():
        version = os.getenv("API_VERSION", "0.0.0")  # Default value if not found
        return jsonify({"version": version})

    @app.route("/")
    def index():
        return "<h1>Welcome to this python app by Miriam C. Palanca</h1><p>You can check the version of the app with /version and /temperature to check the hivebox status.</p>"
        #return redirect("http://localhost/index.php") with nginx
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
