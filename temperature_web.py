from flask import Flask, render_template_string
import firebase_admin
from firebase_admin import credentials, firestore
import time
import os
import json
from flask import redirect



# 🔐 Inicializar Firebase
firebase_key_json = os.environ["FIREBASE_KEY"]
cred = credentials.Certificate(json.loads(firebase_key_json))
firebase_admin.initialize_app(cred)
db = firestore.client()

# 🚀 Iniciar app Flask
app = Flask(__name__)

# HTML embebido
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Sensor {{ sensor_id }}</title>
    <meta http-equiv="refresh" content="3">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f8;
            padding: 2rem;
        }
        .card {
            background: white;
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 0 12px rgba(0,0,0,0.1);
            max-width: 400px;
            margin: auto;
        }
        h2 {
            margin-bottom: 1rem;
        }
        .metric {
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>🔍 Sensor: {{ sensor_id }}</h2>
        <div class="metric">🌡 <b>Temperatura:</b> {{ data.temperature }} °C</div>
        <div class="metric">💧 <b>Humedad:</b> {{ data.humidity }} %</div>
        <div class="metric">🔽 <b>Presión:</b> {{ data.pressure }} hPa</div>
        <div class="metric">🧪 <b>Gas:</b> {{ data.gas }} Ω</div>
        <div class="metric"><small>⏱ {{ timestamp }}</small></div>
    </div>
</body>
</html>
"""

@app.route('/stream/<sensor_id>')
def stream(sensor_id):
    doc = db.collection("temperature").document(sensor_id).get()
    if not doc.exists:
        return f"No hay datos para {sensor_id}", 404
    
    data = doc.to_dict()
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data.get("timestamp", 0)))
    
    return render_template_string(
        HTML_TEMPLATE,
        sensor_id=sensor_id,
        data=data,
        timestamp=ts
    )

@app.route("/")
def index():
     return redirect("/stream/TEMP_RPI_BME680")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
