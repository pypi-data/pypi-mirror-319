import aiohttp

class AutoModerationManager:
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

    async def create_rule(self, guild_id, name, event_type, trigger_type, trigger_metadata, actions, exempt_roles=None, exempt_channels=None):
        url = f"{self.base_url}/guilds/{guild_id}/auto-moderation/rules"
        payload = {
            "name": name,
            "event_type": event_type,
            "trigger_type": trigger_type,
            "trigger_metadata": trigger_metadata,
            "actions": actions,
            "exempt_roles": exempt_roles or [],
            "exempt_channels": exempt_channels or []
        }
        async with self.session.post(url, json=payload) as response:
            if response.status in {200, 201}:
                return await response.json()
            else:
                print(f"Failed to create rule: {response.status} - {await response.text()}")
                return None

    async def get_rules(self, guild_id):
        url = f"{self.base_url}/guilds/{guild_id}/auto-moderation/rules"
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to fetch rules: {response.status} - {await response.text()}")
                return None

    async def get_rule(self, guild_id, rule_id):
        url = f"{self.base_url}/guilds/{guild_id}/auto-moderation/rules/{rule_id}"
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to fetch rule: {response.status} - {await response.text()}")
                return None

    async def modify_rule(self, guild_id, rule_id, name=None, enabled=None, actions=None):
        url = f"{self.base_url}/guilds/{guild_id}/auto-moderation/rules/{rule_id}"
        data = {}
        if name:
            data["name"] = name
        if enabled is not None:
            data["enabled"] = enabled
        if actions:
            data["actions"] = actions

        async with self.session.patch(url, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to modify rule: {response.status} - {await response.text()}")
                return None

    async def delete_rule(self, guild_id, rule_id):
        url = f"{self.base_url}/guilds/{guild_id}/auto-moderation/rules/{rule_id}"
        async with self.session.delete(url) as response:
            if response.status == 204:
                print(f"Rule {rule_id} deleted successfully.")
                return True
            else:
                print(f"Failed to delete rule: {response.status} - {await response.text()}")
                return False
