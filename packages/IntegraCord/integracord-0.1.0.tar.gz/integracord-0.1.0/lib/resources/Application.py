import aiohttp

class ApplicationManager:
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

    async def get_application_details(self):
        url = f"{self.base_url}/applications/{self.application_id}"
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to fetch application details: {response.status} - {await response.text()}")
                return None

    async def update_application(self, **kwargs):
        url = f"{self.base_url}/applications/@me"
        async with self.session.patch(url, json=kwargs) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to update application: {response.status} - {await response.text()}")
                return None
