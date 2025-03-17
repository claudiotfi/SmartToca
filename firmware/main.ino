#include <WiFi.h>
#include <PubSubClient.h>

// Definição dos pinos dos sensores
#define TEMP_SENSOR_PIN A0
#define HUM_SENSOR_PIN A1
#define WATER_LEVEL_PIN A2
#define ENERGY_SENSOR_PIN A3
#define RELAY_PIN 5  // Exemplo de controle de atuador

// Configuração de Wi-Fi
const char* ssid = "SEU_WIFI";
const char* password = "SUA_SENHA";

// Configuração do MQTT
const char* mqtt_server = "192.168.1.100"; // IP do Mini-PC
const int mqtt_port = 1883;
const char* mqtt_user = "usuario";
const char* mqtt_password = "senha";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
    Serial.begin(115200);
    
    // Conectar ao Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConectado ao Wi-Fi!");

    // Conectar ao servidor MQTT
    client.setServer(mqtt_server, mqtt_port);
    client.setCallback(mqttCallback);

    while (!client.connected()) {
        Serial.print("Conectando ao MQTT...");
        if (client.connect("STM32_Client", mqtt_user, mqtt_password)) {
            Serial.println("Conectado!");
            client.subscribe("home/commands");  // Receber comandos do backend
        } else {
            Serial.print("Falha, código: ");
            Serial.println(client.state());
            delay(5000);
        }
    }

    pinMode(RELAY_PIN, OUTPUT);
}

// Função para processar comandos do backend
void mqttCallback(char* topic, byte* payload, unsigned int length) {
    String message;
    for (int i = 0; i < length; i++) {
        message += (char)payload[i];
    }

    Serial.print("Comando recebido: ");
    Serial.println(message);

    if (message == "ligar_bomba") {
        digitalWrite(RELAY_PIN, HIGH);
    } else if (message == "desligar_bomba") {
        digitalWrite(RELAY_PIN, LOW);
    }
}

// Leitura dos sensores
void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();

    int temperatura = analogRead(TEMP_SENSOR_PIN);
    int umidade = analogRead(HUM_SENSOR_PIN);
    int nivel_agua = analogRead(WATER_LEVEL_PIN);
    int consumo = analogRead(ENERGY_SENSOR_PIN);

    String payload = "{";
    payload += "\"temperatura\":" + String(temperatura) + ",";
    payload += "\"umidade\":" + String(umidade) + ",";
    payload += "\"nivel_agua\":" + String(nivel_agua) + ",";
    payload += "\"consumo\":" + String(consumo);
    payload += "}";

    client.publish("home/sensores", payload.c_str());

    delay(5000); // Enviar dados a cada 5 segundos
}

// Reconectar ao MQTT caso a conexão caia
void reconnect() {
    while (!client.connected()) {
        Serial.print("Reconectando ao MQTT...");
        if (client.connect("STM32_Client", mqtt_user, mqtt_password)) {
            Serial.println("Reconectado!");
            client.subscribe("home/commands");
        } else {
            Serial.print("Falha, código: ");
            Serial.println(client.state());
            delay(5000);
        }
    }
}
