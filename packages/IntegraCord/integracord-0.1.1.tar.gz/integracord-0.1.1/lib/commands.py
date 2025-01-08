import aiohttp
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
APPLICATION_ID = os.getenv("APPLICATION_ID")
GLOBAL_COMMANDS_URL = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/commands"

async def register_global_commands(handler):
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(GLOBAL_COMMANDS_URL) as response:
            if response.status == 200:
                existing_commands = await response.json()
                existing_commands_map = {cmd["name"]: cmd for cmd in existing_commands}
            else:
                print("Failed to fetch global commands:", await response.json())
                return

        for name, details in handler.commands.items():
            payload = {
                "name": name,
                "description": details["description"],
                "options": details.get("options", [])
            }

            if name in existing_commands_map:
                existing_command = existing_commands_map[name]
                if payload["description"] == existing_command["description"] and payload["options"] == existing_command.get("options", []):
                    print(f"Command '{name}' is already up-to-date. Skipping.")
                    continue

            print(f"Registering or updating command: {payload}")
            async with session.post(GLOBAL_COMMANDS_URL, json=payload) as response:
                if response.status == 201:
                    print(f"Command '{name}' registered successfully!")
                elif response.status == 429:
                    retry_after = int(response.headers.get("Retry-After", 1))
                    print(f"Rate limit hit. Retrying after {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                    continue
                else:
                    print(f"Failed to register command '{name}': {response.status}")
                    response_data = await response.json()
                    print("Response JSON:", response_data)

        existing_command_names = set(existing_commands_map.keys())
        handler_command_names = set(handler.commands.keys())
        commands_to_delete = existing_command_names - handler_command_names

        for command_name in commands_to_delete:
            command_id = existing_commands_map[command_name]["id"]
            delete_url = f"{GLOBAL_COMMANDS_URL}/{command_id}"
            async with session.delete(delete_url) as delete_response:
                if delete_response.status == 204:
                    print(f"Deleted global command '{command_name}' successfully!")
                elif delete_response.status == 429:
                    retry_after = int(delete_response.headers.get("Retry-After", 1))
                    print(f"Rate limit hit during delete. Retrying after {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                else:
                    print(f"Failed to delete global command '{command_name}': {delete_response.status}")


