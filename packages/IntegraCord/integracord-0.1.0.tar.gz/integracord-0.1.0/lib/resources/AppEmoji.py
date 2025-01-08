import aiohttp

class AppEmojiManager:
    def __init__(self, token, application_id):
        self.token = token
        self.application_id = application_id
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

    async def list_application_emojis(self):
        url = f"{self.base_url}/applications/{self.application_id}/emojis"
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to list emojis: {response.status} - {await response.text()}")
                return None

    async def get_application_emoji(self, emoji_id):
        url = f"{self.base_url}/applications/{self.application_id}/emojis/{emoji_id}"
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to retrieve emoji: {response.status} - {await response.text()}")
                return None

    async def create_application_emoji(self, name, image_data):
        url = f"{self.base_url}/applications/{self.application_id}/emojis"
        data = {
            "name": name,
            "image": image_data
        }
        async with self.session.post(url, json=data) as response:
            if response.status == 201:
                return await response.json()
            else:
                print(f"Failed to create emoji: {response.status} - {await response.text()}")
                return None

    async def modify_application_emoji(self, emoji_id, name=None, image_data=None):
        url = f"{self.base_url}/applications/{self.application_id}/emojis/{emoji_id}"
        data = {}
        if name:
            data["name"] = name
        if image_data:
            data["image"] = image_data
        async with self.session.patch(url, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to modify emoji: {response.status} - {await response.text()}")
                return None

    async def delete_application_emoji(self, emoji_id):
        url = f"{self.base_url}/applications/{self.application_id}/emojis/{emoji_id}"
        async with self.session.delete(url) as response:
            if response.status == 204:
                print(f"Emoji {emoji_id} deleted successfully.")
                return True
            else:
                print(f"Failed to delete emoji: {response.status} - {await response.text()}")
                return False
