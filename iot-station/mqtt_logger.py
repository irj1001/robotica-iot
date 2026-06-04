import paho.mqtt.client as mqtt
import csv
from datetime import datetime
import os
import json

TOPIC = "iot/desk/temperature"
CSV_FILE = "data.csv"

# =========================
# INIT CSV (multi-sensor ready)
# =========================

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "temperature",
            "humidity",
            "light"
        ])


# =========================
# MQTT CALLBACKS
# =========================

def on_connect(client, userdata, flags, rc):
    print("🔵 Conectado a MQTT")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload = msg.payload.decode()

    temperature = None
    humidity = None
    light = None

    # =========================
    # FORMATO FUTURO (JSON)
    # =========================
    try:
        data = json.loads(payload)

        temperature = data.get("temperature")
        humidity = data.get("humidity")
        light = data.get("light")

    except:
        # =========================
        # FORMATO ACTUAL (solo temp)
        # =========================
        try:
            temperature = float(payload)
        except:
            temperature = None

    print(f"{timestamp} → 🌡 {temperature} | 💧 {humidity} | 💡 {light}")

    # =========================
    # GUARDAR CSV
    # =========================
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            temperature,
            humidity,
            light
        ])


# =========================
# MQTT CLIENT
# =========================

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

print("🚀 Logger IoT activo...")
client.loop_forever()