import aiohttp

class MessageManager:
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

    async def get_message(self, channel_id, message_id):
        url = f"{self.base_url}/channels/{channel_id}/messages/{message_id}"
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Error fetching message: {response.status} {await response.text()}")

    async def create_message(self, channel_id, content, tts=False, embeds=None, allowed_mentions=None):
        url = f"{self.base_url}/channels/{channel_id}/messages"
        data = {
            "content": content,
            "tts": tts,
            "embeds": embeds or [],
            "allowed_mentions": allowed_mentions or {}
        }
        async with self.session.post(url, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Error creating message: {response.status} {await response.text()}")

    async def edit_message(self, channel_id, message_id, content=None, embeds=None, allowed_mentions=None):
        url = f"{self.base_url}/channels/{channel_id}/messages/{message_id}"
        data = {
            "content": content,
            "embeds": embeds or [],
            "allowed_mentions": allowed_mentions or {}
        }
        async with self.session.patch(url, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Error editing message: {response.status} {await response.text()}")

    async def delete_message(self, channel_id, message_id):
        url = f"{self.base_url}/channels/{channel_id}/messages/{message_id}"
        async with self.session.delete(url) as response:
            if response.status == 204:
                print(f"Message {message_id} deleted.")
            else:
                raise Exception(f"Error deleting message: {response.status} {await response.text()}")

    async def add_reaction(self, channel_id, message_id, emoji):
        url = f"{self.base_url}/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
        async with self.session.put(url) as response:
            if response.status == 204:
                print(f"Reaction {emoji} added to message {message_id}.")
            else:
                raise Exception(f"Error adding reaction: {response.status} {await response.text()}")

    async def remove_reaction(self, channel_id, message_id, emoji):
        url = f"{self.base_url}/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
        async with self.session.delete(url) as response:
            if response.status == 204:
                print(f"Reaction {emoji} removed from message {message_id}.")
            else:
                raise Exception(f"Error removing reaction: {response.status} {await response.text()}")

    async def remove_all_reactions(self, channel_id, message_id):
        url = f"{self.base_url}/channels/{channel_id}/messages/{message_id}/reactions"
        async with self.session.delete(url) as response:
            if response.status == 204:
                print(f"All reactions removed from message {message_id}.")
            else:
                raise Exception(f"Error removing all reactions: {response.status} {await response.text()}")

    async def pin_message(self, channel_id, message_id):
        url = f"{self.base_url}/channels/{channel_id}/pins/{message_id}"
        async with self.session.put(url) as response:
            if response.status == 204:
                print(f"Message {message_id} pinned.")
            else:
                raise Exception(f"Error pinning message: {response.status} {await response.text()}")

    async def unpin_message(self, channel_id, message_id):
        url = f"{self.base_url}/channels/{channel_id}/pins/{message_id}"
        async with self.session.delete(url) as response:
            if response.status == 204:
                print(f"Message {message_id} unpinned.")
            else:
                raise Exception(f"Error unpinning message: {response.status} {await response.text()}")

    async def crosspost_message(self, channel_id, message_id):
        url = f"{self.base_url}/channels/{channel_id}/messages/{message_id}/crosspost"
        async with self.session.post(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Error crossposting message: {response.status} {await response.text()}")
