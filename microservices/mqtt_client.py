import paho.mqtt.client as mqtt
import json

# Configurações do MQTT
BROKER = "localhost"  # Ou IP do Mini-PC
PORT = 1883
TOPIC_SUBSCRIBE = "home/automation/#"  # Assina todos os tópicos da casa
TOPIC_PUBLISH = "home/commands/"

# Callback quando a conexão é estabelecida
def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker MQTT com código {rc}")
    client.subscribe(TOPIC_SUBSCRIBE)

# Callback quando uma mensagem é recebida
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"Mensagem recebida em {msg.topic}: {payload}")
        process_message(msg.topic, payload)
    except json.JSONDecodeError:
        print("Erro ao decodificar JSON")

# Processa mensagens recebidas
def process_message(topic, payload):
    if topic == "home/automation/irrigation":
        print("Comando de irrigação recebido")
    elif topic == "home/automation/aquarium":
        print("Comando para aquário recebido")
    # Adicionar mais comandos conforme necessário

# Publica mensagens no MQTT
def publish_message(topic, data):
    payload = json.dumps(data)
    client.publish(topic, payload)
    print(f"Publicado em {topic}: {data}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)

# Loop para manter a conexão ativa
client.loop_forever()