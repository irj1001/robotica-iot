import paho.mqtt.client as mqtt
import json
import csv
import os
from datetime import datetime

# =========================
# CONFIG
# =========================

TOPIC = "iot/desk/temperature"
CSV_FILE = "data.csv"

# =========================
# INIT CSV (si no existe)
# =========================

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "temperature", "humidity", "light"])

# =========================
# MQTT CALLBACKS
# =========================

def on_connect(client, userdata, flags, rc):
    print("🔵 Conectado a MQTT")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()

        # =========================
        # INTENTAR JSON (futuro ESP32)
        # =========================
        try:
            data = json.loads(payload)
            temperature = data.get("temperature")
            humidity = data.get("humidity")
            light = data.get("light")

        # =========================
        # FALLBACK (tu formato actual)
        # =========================
        except:
            try:
                temperature = float(payload)
            except:
                temperature = None
            humidity = None
            light = None

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"🌡 Temp: {temperature} °C | 💧 Hum: {humidity} | 💡 Lux: {light}")

        # =========================
        # GUARDAR CSV
        # =========================
        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                temperature,
                humidity,
                light
            ])

    except Exception as e:
        print("❌ Error procesando mensaje:", e)

# =========================
# CLIENT MQTT
# =========================

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

print("🚀 Esperando datos MQTT...")
client.loop_forever()