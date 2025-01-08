import datetime
import aiohttp

class ModerationManager:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://discord.com/api/v10"
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bot {self.token}",
                "Content-Type": "application/json"
            }
        )

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self.session.close()

    async def ban(self, guild_id, member_id, reason=None):
        url = f"{self.base_url}/guilds/{guild_id}/bans/{member_id}"
        json_data = {"reason": reason} if reason else {}
        async with self.session.put(url, json=json_data) as response:
            if response.status != 204:
                print(f"Failed to ban user: {response.status}")
                return None
            return response

    async def kick(self, guild_id, member_id, reason=None):
        url = f"{self.base_url}/guilds/{guild_id}/members/{member_id}"
        json_data = {"reason": reason} if reason else {}
        async with self.session.delete(url, json=json_data) as response:
            if response.status != 204:
                print(f"Failed to kick user: {response.status}")
                return None
            return response

    async def timeout(self, guild_id, member_id, duration, reason=None):
        url = f"{self.base_url}/guilds/{guild_id}/members/{member_id}"
        json_data = {
            "communication_disabled_until": (datetime.datetime.utcnow() + datetime.timedelta(seconds=duration)).isoformat()
        }
        if reason:
            json_data["reason"] = reason
        async with self.session.patch(url, json=json_data) as response:
            if response.status != 200:
                print(f"Failed to timeout user: {response.status}")
                return None
            return response
