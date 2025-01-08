import aiohttp

class WebhookManager:
    def __init__(self, token):
        self.token = token
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

    async def create_webhook(self, channel_id, name, avatar=None):
        url = f"{self.base_url}/channels/{channel_id}/webhooks"
        data = {
            "name": name,
            "avatar": avatar
        }
        async with self.session.post(url, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to create webhook: {response.status} - {await response.text()}")

    async def edit_webhook(self, webhook_id, name=None, avatar=None, channel_id=None):
        url = f"{self.base_url}/webhooks/{webhook_id}"
        data = {}
        if name:
            data["name"] = name
        if avatar:
            data["avatar"] = avatar
        if channel_id:
            data["channel_id"] = channel_id

        async with self.session.patch(url, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to edit webhook: {response.status} - {await response.text()}")

    async def get_webhook(self, webhook_id):
        url = f"{self.base_url}/webhooks/{webhook_id}"
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to retrieve webhook: {response.status} - {await response.text()}")

    async def delete_webhook(self, webhook_id):
        url = f"{self.base_url}/webhooks/{webhook_id}"
        async with self.session.delete(url) as response:
            if response.status == 204:
                print(f"Webhook {webhook_id} deleted successfully.")
            else:
                raise Exception(f"Failed to delete webhook: {response.status} - {await response.text()}")

    async def send_webhook_message(self, webhook_id, webhook_token, content, embeds=None, username=None, avatar_url=None):
        url = f"{self.base_url}/webhooks/{webhook_id}/{webhook_token}"
        data = {
            "content": content,
            "embeds": embeds or [],
            "username": username,
            "avatar_url": avatar_url
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status in (200, 204):
                    print("Message sent successfully.")
                else:
                    raise Exception(f"Failed to send message: {response.status} - {await response.text()}")
