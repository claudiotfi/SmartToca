import serial
import paho.mqtt.client as mqtt
import time

# Configurações
SERIAL_PORT = "/dev/ttyUSB0"  # Ajuste conforme necessário
BAUD_RATE = 115200
MQTT_BROKER = "localhost"
MQTT_TOPIC_SENSOR = "aquarium/sensors"
MQTT_TOPIC_CONTROL = "aquarium/control"

# Conectar ao STM32 via Serial
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def on_connect(client, userdata, flags, rc):
    print("Conectado ao MQTT Broker com código:", rc)
    client.subscribe(MQTT_TOPIC_CONTROL)

def on_message(client, userdata, msg):
    comando = msg.payload.decode()
    print(f"Comando recebido: {comando}")
    ser.write((comando + "\n").encode())  # Enviar comando ao STM32

# Configurar MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.loop_start()

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            print(f"Dados recebidos: {data}")
            mqtt_client.publish(MQTT_TOPIC_SENSOR, data)
        time.sleep(1)
except KeyboardInterrupt:
    print("Finalizando...")
    ser.close()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()