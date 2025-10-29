import asyncio

import websockets


async def client():
    uri = "ws://localhost:8765"  # Адрес сервера
    async with websockets.connect(uri) as websocket:
        print("🔗 Подключено к серверу! (введи 'exit' для выхода)\n")

        while True:
            message = input("Вы: ")
            if message.lower() in ("exit", "quit"):
                print("👋 Завершаем соединение...")
                break

            # Отправляем сообщение
            await websocket.send(message)
            print(f"📤 Отправлено: {message}")

            # Получаем ответ сразу после отправки
            response = await websocket.recv()
            print(f"📥 Ответ от сервера: {response}\n")

asyncio.run(client())
