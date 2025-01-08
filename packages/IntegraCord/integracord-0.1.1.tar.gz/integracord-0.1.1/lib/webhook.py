from fastapi import FastAPI, Request, HTTPException
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import json
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

class Webhook:
    def __init__(self):
        self.verify_key = VerifyKey(bytes.fromhex(os.getenv("APPLICATION_PUBLIC_KEY")))

    async def validate_request(self, request: Request):
        signature = request.headers.get("X-Signature-Ed25519")
        timestamp = request.headers.get("X-Signature-Timestamp")
        body = await request.body()

        try:
            self.verify_key.verify(f'{timestamp}{body.decode()}'.encode(), bytes.fromhex(signature))
        except BadSignatureError:
            raise HTTPException(status_code=401, detail="Invalid request signature")

        return json.loads(body)

    async def handle_ping(self, payload: dict):
        if payload.get("type") == 1:
            return {"type": 1}

webhook = Webhook()
