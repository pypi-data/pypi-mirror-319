# IntegraCord

IntegraCord that allows you to connect to the application as a "Webhook" without connecting to the Discord gateway.

## Setup
1. Download repository `pip install IntegraCord`.
2. Create an `.env` file for configuration and enter:
```env
BOT_TOKEN=TOKEN # The bot token is needed for integration with the discord API, e.g. channel creation and so on
APPLICATION_ID=ID
APPLICATION_PUBLIC_KEY=KEY
```
3. Create a startup file, e.g. main.py, and enter this script:
```py
from fastapi import FastAPI, Request
from IntegraCord.lib.webhook import webhook
from IntegraCord.lib.handler import InteractionHandler
from IntegraCord.lib.commands import register_global_commands
from IntegraCord.lib.utils import send_message

import asyncio

app = FastAPI()
handler = InteractionHandler()

async def setup_commands():
    await register_global_commands(handler)

@handler.command(name="ping", description="ping pong")
async def ping_command(payload):
    return send_message('pong')

@app.post("/interactions")
async def interactions(request: Request):
    payload = await webhook.validate_request(request)

    if payload.get("type") == 1:
        return await webhook.handle_ping(payload)

    return await handler.handle_interaction(payload)

if __name__ == "__main__":
    import uvicorn
    asyncio.run(setup_commands())
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
4. Run and wait for the script to register the commands, and open the local network.
5. It is necessary to give your own endpoint to the application panel on the discord website, so if you have `ngrok` then run the command `ngrok http 0.0.0.0:8000`. If you do not have one then install it.
6. If all goes according to plan, copy the displayed link in the console from ngrok and paste it into the `Interactions Endpoint URL`, as in the following screenshot:
![image](https://github.com/user-attachments/assets/d86056ca-c40d-4cdd-8e2a-a2158ca0e71a)

## Additional notes
The library is under development, all the points mentioned in the Setup should make your bot responsive to ngrok integrations. If you don't see the command on your own server, reset Discord (CTRL + R).
