import paho.mqtt.client as mqtt
import time
import serial
import json

# Configurações do STM32 (porta serial)
SERIAL_PORT = '/dev/ttyUSB0'  # Ajuste conforme necessário
BAUD_RATE = 115200

# Configurações do MQTT
MQTT_BROKER = "mqtt.example.com"
MQTT_TOPIC_SENSORS = "home/aquaponics/sensors"
MQTT_TOPIC_COMMANDS = "home/aquaponics/commands"

# Inicializa comunicação serial com STM32
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def on_connect(client, userdata, flags, rc):
    print("Conectado ao MQTT Broker!")
    client.subscribe(MQTT_TOPIC_COMMANDS)

def on_message(client, userdata, msg):
    command = msg.payload.decode()
    print(f"Comando recebido: {command}")
    
    # Envia comando para o STM32 via serial
    ser.write((command + "\n").encode())

def read_sensors():
    """Lê dados do STM32 via serial e publica no MQTT."""
    if ser.in_waiting > 0:
        try:
            data = ser.readline().decode().strip()
            sensor_data = json.loads(data)  # STM32 envia JSON
            client.publish(MQTT_TOPIC_SENSORS, json.dumps(sensor_data))
            print("Dados enviados:", sensor_data)
        except Exception as e:
            print("Erro ao processar dados do STM32:", e)

# Configuração do cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.loop_start()

print("Sistema de Aquaponia iniciado...")

# Loop principal
try:
    while True:
        read_sensors()
        time.sleep(5)  # Ajuste conforme necessário
except KeyboardInterrupt:
    print("Finalizando...")
    client.loop_stop()
    ser.close()
