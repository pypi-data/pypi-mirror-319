import aiohttp

class EntitlementManager:
    def __init__(self, token, application_id,):
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

    async def list_entitlements(self, sku_ids=None, user_id=None, guild_id=None):
        params = {"application_id": self.application_id}
        if sku_ids:
            params["sku_ids"] = ",".join(sku_ids)
        if user_id:
            params["user_id"] = user_id
        if guild_id:
            params["guild_id"] = guild_id

        url = f"{self.base_url}/entitlements"
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to list entitlements: {response.status} - {await response.text()}")
                return None

    async def consume_entitlement(self, entitlement_id):
        url = f"{self.base_url}/entitlements/{entitlement_id}/consume"
        async with self.session.post(url) as response:
            if response.status == 204:
                print(f"Entitlement {entitlement_id} consumed successfully.")
                return True
            else:
                print(f"Failed to consume entitlement: {response.status} - {await response.text()}")
                return False

    async def create_test_entitlement(self, sku_id, user_id, guild_id=None):
        url = f"{self.base_url}/entitlements/test-entitlements"
        data = {
            "application_id": self.application_id,
            "sku_id": sku_id,
            "user_id": user_id,
            "guild_id": guild_id
        }

        async with self.session.post(url, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to create test entitlement: {response.status} - {await response.text()}")
                return None

    async def delete_test_entitlement(self, entitlement_id):
        url = f"{self.base_url}/entitlements/test-entitlements/{entitlement_id}"
        async with self.session.delete(url) as response:
            if response.status == 204:
                print(f"Test entitlement {entitlement_id} deleted successfully.")
                return True
            else:
                print(f"Failed to delete test entitlement: {response.status} - {await response.text()}")
                return False
