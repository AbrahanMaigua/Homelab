# consola/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import subprocess

class ConsolaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Lógica para manejar la conexión WebSocket
        self.room_group_name = "consola"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Lógica para manejar la desconexión
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Recibe el comando desde el cliente WebSocket
        data = json.loads(text_data)
        comando = data.get('comando')

        if comando and comando.startswith("img "):
            src = comando.split(' ')[-1].replace('\\', '/',)
            if not src.startswith('http'):
                src = 'http://localhost:8000/media/imagenes/' + src.split('/')[-1]
            img = f"<img src='{src}' alt='Imagen cargada'>"
            await self.send(text_data=json.dumps({
                'resultado': img
            }))
        else:
            try:
                resultado = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT, text=True)
                await self.send(text_data=json.dumps({
                    'resultado': resultado
                }))
            except subprocess.CalledProcessError as e:
                await self.send(text_data=json.dumps({
                    'error': f"Error ejecutando el comando: {e.output}"
                }))
            except Exception as e:
                await self.send(text_data=json.dumps({
                    'error': f"Ocurrió un error inesperado: {str(e)}"
                }))
