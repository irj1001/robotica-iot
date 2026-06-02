#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "MOVISTAR_FB08";
const char* password = "E9C94tTpq39rVPm9vvqx";

const char* mqtt_server = "192.168.1.68"; 

WiFiClient espClient;
PubSubClient client(espClient);

const int TMP_PIN = 4;

void setup_wifi() {
  delay(10);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void reconnect() {
  while (!client.connected()) {
    client.connect("esp32-temp");
    delay(500);
  }
}

float readTemp() {
  int raw = analogRead(TMP_PIN);
  float voltage = raw * (3.3 / 4095.0);
  return (voltage - 0.5) * 100.0;
}

void setup() {
  Serial.begin(115200);
  setup_wifi();

  client.setServer(mqtt_server, 1883);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  float temp = readTemp();

  char msg[50];
  sprintf(msg, "%.2f", temp);

  client.publish("iot/desk/temperature", msg);

  Serial.println(msg);

  delay(2000);
}