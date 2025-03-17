import asyncio
import websockets
import json
from database import save_sensor_data

# Configurações
HOST = '0.0.0.0'  # Acessível em toda a rede
PORT = 8765  # Porta WebSocket

# Lista de clientes conectados
clients = set()

async def handle_connection(websocket, path):
    """Gerencia conexões WebSocket e recebe dados dos sensores."""
    global clients
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Recebido: {data}")
            
            # Salvar no banco de dados
            save_sensor_data(data)
            
            # Reenviar os dados para todos os clientes conectados
            await broadcast(json.dumps(data))
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)

async def broadcast(message):
    """Envia uma mensagem para todos os clientes conectados."""
    if clients:
        await asyncio.wait([client.send(message) for client in clients])

async def main():
    """Inicializa o servidor WebSocket."""
    async with websockets.serve(handle_connection, HOST, PORT):
        print(f"Servidor WebSocket iniciado em ws://{HOST}:{PORT}")
        await asyncio.Future()  # Mantém o servidor rodando

if __name__ == "__main__":
    asyncio.run(main())
