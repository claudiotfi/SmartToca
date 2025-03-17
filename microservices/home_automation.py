import time
import json
import paho.mqtt.client as mqtt
from database import insert_sensor_data, insert_log

# Configurações MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_SENSORS = "home/sensors"
MQTT_TOPIC_ACTUATORS = "home/actuators"

# Callback para quando recebe mensagens MQTT
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    sensor = payload.get("sensor")
    value = payload.get("value")
    
    if sensor and value is not None:
        insert_sensor_data(sensor, value)
        print(f"Sensor {sensor}: {value}")
        
        # Ações automáticas
        if sensor == "gas_leak" and value > 0:
            print("🚨 Vazamento de gás detectado! Acionando exaustor!")
            client.publish(MQTT_TOPIC_ACTUATORS, json.dumps({"device": "exaustor", "state": "ON"}))
            insert_log("Gas leak detected. Exhaust fan activated.")
        elif sensor == "mailbox" and value == 1:
            print("📬 Correio: Nova correspondência recebida!")
            insert_log("New mail detected.")

# Configuração do cliente MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC_SENSORS)
client.loop_start()

# Loop principal para monitoramento
def main():
    print("🏠 Automação Residencial Iniciada")
    try:
        while True:
            time.sleep(1)  # Aguarda novas mensagens MQTT
    except KeyboardInterrupt:
        print("Desligando automação...")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
