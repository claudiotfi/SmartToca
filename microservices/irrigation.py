import time
import json
import paho.mqtt.client as mqtt
from database import insert_sensor_data, get_latest_sensor_value

# Configurações
MQTT_BROKER = "localhost"
MQTT_TOPIC_SENSOR = "home/irrigation/soil_moisture"
MQTT_TOPIC_VALVE = "home/irrigation/valve"
MOISTURE_THRESHOLD = 30  # Umidade abaixo disso aciona a irrigação

# Callback para recebimento de mensagens MQTT
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        sensor_id = payload.get("sensor_id")
        moisture = payload.get("moisture")
        timestamp = payload.get("timestamp", time.time())
        
        if sensor_id and moisture is not None:
            insert_sensor_data(sensor_id, "soil_moisture", moisture, timestamp)
            print(f"Umidade do solo recebida: {moisture}%")
            check_irrigation(moisture)
    except Exception as e:
        print(f"Erro ao processar mensagem MQTT: {e}")

# Função para verificar e acionar a irrigação
def check_irrigation(moisture):
    if moisture < MOISTURE_THRESHOLD:
        print("Umidade baixa! Acionando irrigação...")
        mqtt_client.publish(MQTT_TOPIC_VALVE, json.dumps({"action": "open"}))
    else:
        print("Solo adequado. Mantendo válvula fechada.")
        mqtt_client.publish(MQTT_TOPIC_VALVE, json.dumps({"action": "close"}))

# Configuração do cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.subscribe(MQTT_TOPIC_SENSOR)
mqtt_client.loop_start()

print("Sistema de irrigação iniciado...")

# Loop principal
try:
    while True:
        time.sleep(10)  # Aguarda novos dados
except KeyboardInterrupt:
    print("Encerrando sistema de irrigação...")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()