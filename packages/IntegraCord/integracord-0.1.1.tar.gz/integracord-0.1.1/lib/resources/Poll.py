import aiohttp

class PollManager:
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

    async def create_poll(self, channel_id, question, answers, duration=None, allow_multiselect=False, layout_type=1):
        url = f"{self.base_url}/channels/{channel_id}/messages"
        data = {
            "content": "New Poll",
            "poll": {
                "question": {"text": question},
                "answers": [{"text": answer} for answer in answers],
                "allow_multiselect": allow_multiselect,
                "layout_type": layout_type,
            }
        }

        if duration:
            data["poll"]["duration"] = duration * 3600

        async with self.session.post(url, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to create poll: {response.status} - {await response.text()}")
                return None

    async def get_answer_voters(self, channel_id, message_id, answer_id, limit=25, after=None):
        url = f"{self.base_url}/channels/{channel_id}/polls/{message_id}/answers/{answer_id}"
        params = {"limit": limit}
        if after:
            params["after"] = after

        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to retrieve answer voters: {response.status} - {await response.text()}")
                return None

    async def end_poll(self, channel_id, message_id):
        url = f"{self.base_url}/channels/{channel_id}/polls/{message_id}/expire"
        async with self.session.post(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to end poll: {response.status} - {await response.text()}")
                return None

    async def get_poll_results(self, channel_id, message_id):
        url = f"{self.base_url}/channels/{channel_id}/polls/{message_id}"
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to retrieve poll results: {response.status} - {await response.text()}")
                return None

    async def delete_poll(self, channel_id, message_id):
        url = f"{self.base_url}/channels/{channel_id}/polls/{message_id}"
        async with self.session.delete(url) as response:
            if response.status == 204:
                print(f"Poll {message_id} deleted successfully.")
                return True
            else:
                print(f"Failed to delete poll: {response.status} - {await response.text()}")
                return False
