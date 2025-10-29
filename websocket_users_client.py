import asyncio

import websockets


async def client():
    uri = "ws://localhost:8765"  # Адрес сервера
    async with websockets.connect(uri) as websocket:
        message = input()  # Сообщение, которое отправит клиент
        print(f"Отправка: {message}")
        await websocket.send(message)  # Отправляем сообщение

        for _ in range(5):
            response = await websocket.recv()
            print(f"Ответ от сервера: {response}")

asyncio.run(client())
