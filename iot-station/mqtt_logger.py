import paho.mqtt.client as mqtt
import csv
from datetime import datetime
import os

TOPIC = "iot/desk/temperature"
CSV_FILE = "data.csv"

# crear archivo si no existe
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "temperature"])


def on_connect(client, userdata, flags, rc):
    print("Conectado a MQTT")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    temp = msg.payload.decode()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"{timestamp} → {temp} °C")

    # guardar en CSV
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, temp])


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()