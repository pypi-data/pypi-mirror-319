import aiohttp

class GuildManager:
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

    async def fetch_member(self, user_id):
        url = f"{self.base_url}/guilds/{self.guild_id}/members/{user_id}"
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to fetch member {user_id}: {response.status} - {await response.text()}")
                return None

    async def fetch_guild(self):
        url = f"{self.base_url}/guilds/{self.guild_id}"
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to fetch guild {self.guild_id}: {response.status} - {await response.text()}")
                return None

    @staticmethod
    def get_display_name(member_data):
        return member_data.get('nick') or member_data['user']['username']

    @staticmethod
    def get_username(member_data):
        return member_data['user']['username']

    @staticmethod
    def get_profile_avatar(member_data):
        avatar = member_data['user'].get('avatar')
        if avatar:
            return f"https://cdn.discordapp.com/avatars/{member_data['user']['id']}/{avatar}.png"
        return None
