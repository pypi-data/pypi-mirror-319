import aiohttp
import asyncio


class VoiceManager:
    def __init__(self, token, user_id, guild_id, channel_id):
        self.token = token
        self.user_id = user_id
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.endpoint = None
        self.session_id = None
        self.ws = None
        self.udp = None
        self.voice_token = None
        self.session = aiohttp.ClientSession(headers={
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        })

    async def connect_to_voice_channel(self, endpoint, session_id, voice_token):
        self.endpoint = endpoint.replace("wss://", "").split(":")[0]
        self.session_id = session_id
        self.voice_token = voice_token

        self.ws = await self.session.ws_connect(f"wss://{self.endpoint}/?v=4")

        await self.ws.send_json({
            "op": 0,
            "d": {
                "server_id": self.guild_id,
                "user_id": self.user_id,
                "session_id": self.session_id,
                "token": self.voice_token,
            }
        })

        asyncio.create_task(self.listen())

    async def join_voice_channel(self):
        url = f"https://discord.com/api/v10/guilds/{self.guild_id}/voice-states/@me"
        payload = {
            "channel_id": self.channel_id
        }

        async with self.session.patch(url, json=payload) as response:
            if response.status == 204:
                print(f"Successfully joined voice channel: {self.channel_id}")
            else:
                print(f"Failed to join voice channel: {response.status}")
                print(await response.text())
                return

        # Dodanie opóźnienia, aby Discord mógł zsynchronizować stan głosowy
        await asyncio.sleep(1)

        # Rozpoczęcie połączenia z Voice Gateway (opcjonalne)
        # Tu możesz dodać logikę połączenia z Voice Gateway

    async def close(self):
        await self.session.close()
    async def listen(self):
        async for message in self.ws:
            data = message.json()
            print("Voice Gateway message:", data)

            if data['op'] == 8:
                print("Voice Gateway Heartbeat ACK received")

    async def start_heartbeat(self, interval):
        while True:
            await asyncio.sleep(interval / 1000)
            await self.ws.send_json({"op": 3, "d": None})

    async def disconnect(self):
        if self.ws:
            await self.ws.close()
            self.ws = None

        await self.session.close()  # Zamykamy sesję, aby uniknąć wycieków
