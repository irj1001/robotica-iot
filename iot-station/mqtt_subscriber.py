import paho.mqtt.client as mqtt

TOPIC = "iot/desk/temperature"

def on_connect(client, userdata, flags, rc):
    print("Conectado a MQTT")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    temp = msg.payload.decode()
    print(f"Temperatura: {temp} °C")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()