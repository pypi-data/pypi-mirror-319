import aiohttp

class ChannelManager:
    def __init__(self, token, guild_id):
        self.token = token
        self.guild_id = guild_id
        self.base_url = "https://discord.com/api/v10"
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bot {self.token}",
                "Content-Type": "application/json"
            }
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def create_channel(self, name, type_):
        url = f"{self.base_url}/guilds/{self.guild_id}/channels"
        json_data = {"name": name, "type": type_}
        async with self.session.post(url, json=json_data) as response:
            if response.status == 201:
                return await response.json()
            else:
                print(f"Failed to create channel: {response.status} - {await response.text()}")
                return None

    async def edit_channel(self, channel_id, new_name):
        url = f"{self.base_url}/channels/{channel_id}"
        json_data = {"name": new_name}
        async with self.session.patch(url, json=json_data) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to edit channel: {response.status} - {await response.text()}")
                return None

    async def delete_channel(self, channel_id):
        url = f"{self.base_url}/channels/{channel_id}"
        async with self.session.delete(url) as response:
            if response.status == 204:
                return {"status": "Channel deleted successfully"}
            else:
                print(f"Failed to delete channel: {response.status} - {await response.text()}")
                return None

    async def list_channels(self):
        url = f"{self.base_url}/guilds/{self.guild_id}/channels"
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to list channels: {response.status} - {await response.text()}")
                return None
