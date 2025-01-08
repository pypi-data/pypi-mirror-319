import aiohttp

class InviteManager:
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

    async def create_invite(self, channel_id, max_age=86400, max_uses=0, temporary=False, unique=True):
        url = f"{self.base_url}/channels/{channel_id}/invites"
        payload = {
            "max_age": max_age,
            "max_uses": max_uses,
            "temporary": temporary,
            "unique": unique
        }

        try:
            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Failed to create invite: {response.status} {await response.text()}")
                    return None
        except Exception as e:
            print(f"Error while creating invite: {e}")
            return None

    async def delete_invite(self, invite_code):
        url = f"{self.base_url}/invites/{invite_code}"

        try:
            async with self.session.delete(url) as response:
                if response.status == 204:
                    print(f"Invite {invite_code} deleted successfully.")
                    return True
                else:
                    print(f"Failed to delete invite: {response.status} {await response.text()}")
                    return False
        except Exception as e:
            print(f"Error while deleting invite: {e}")
            return False

    async def get_invite(self, invite_code):
        url = f"{self.base_url}/invites/{invite_code}"

        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Failed to get invite info: {response.status} {await response.text()}")
                    return None
        except Exception as e:
            print(f"Error while fetching invite info: {e}")
            return None

    async def get_channel_invites(self, channel_id):
        url = f"{self.base_url}/channels/{channel_id}/invites"

        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Failed to get channel invites: {response.status} {await response.text()}")
                    return None
        except Exception as e:
            print(f"Error while fetching channel invites: {e}")
            return None
