import aiohttp

class EmojiManager:
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

    async def get_emojis(self):
        url = f"{self.base_url}/guilds/{self.guild_id}/emojis"
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to get emojis: {response.status} {await response.text()}")
                return None

    async def add_emoji(self, name, image_base64):
        url = f"{self.base_url}/guilds/{self.guild_id}/emojis"
        json_data = {
            "name": name,
            "image": image_base64
        }
        async with self.session.post(url, json=json_data) as response:
            if response.status == 201:
                print(f"Successfully added emoji: {name}")
                return await response.json()
            else:
                print(f"Failed to add emoji: {response.status} {await response.text()}")
                return None

    async def update_emoji(self, emoji_id, name=None, image_base64=None):
        url = f"{self.base_url}/guilds/{self.guild_id}/emojis/{emoji_id}"
        json_data = {}
        if name:
            json_data["name"] = name
        if image_base64:
            json_data["image"] = image_base64

        async with self.session.patch(url, json=json_data) as response:
            if response.status == 200:
                print(f"Successfully updated emoji: {emoji_id}")
                return await response.json()
            else:
                print(f"Failed to update emoji: {response.status} {await response.text()}")
                return None

    async def delete_emoji(self, emoji_id):
        url = f"{self.base_url}/guilds/{self.guild_id}/emojis/{emoji_id}"
        async with self.session.delete(url) as response:
            if response.status == 204:
                print(f"Successfully deleted emoji: {emoji_id}")
                return True
            else:
                print(f"Failed to delete emoji: {response.status} {await response.text()}")
                return False
