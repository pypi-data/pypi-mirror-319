class InteractionHandler:
    def __init__(self):
        self.handlers = {}
        self.commands = {}

    def register_handler(self, name: str, handler, description: str, options: list = None):
        self.handlers[name] = handler
        self.commands[name] = {
            "description": description,
            "options": options or []
        }

    def command(self, name: str, description: str, options: list = None):
        def decorator(func):
            self.register_handler(name, func, description, options)
            print(f"Registered command '{name}': {description}, Options: {options}")
            return func
        return decorator
    
    @staticmethod
    def permissions(**required_permissions):
        def wrapper(func):
            async def wrapped_func(interaction, *args, **kwargs):
                print(f"Interaction payload: {interaction}")

                member = interaction.get("member")
                if not member or "permissions" not in member:
                    return {
                        "type": 4,
                        "data": {
                            "content": "Unable to verify permissions."
                        }
                    }
                user_permissions = int(member["permissions"], 10)
                print(f"User permissions (as int): {user_permissions}")

                missing_permissions = [
                    perm_name
                    for perm_name, required in required_permissions.items()
                    if required and not (user_permissions & (1 << int(required)))
                ]

                if missing_permissions:
                    return {
                        "type": 4,
                        "data": {
                            "content": f"Missing required permissions: {', '.join(missing_permissions)}"
                        }
                    }

                return await func(interaction, *args, **kwargs)

            return wrapped_func
        return wrapper



    async def handle_interaction(self, payload: dict):
        print(f"Received payload: {payload}")
        if "data" in payload and "name" in payload["data"]:
            command_name = payload["data"]["name"]
            options = {
                opt["name"]: opt["value"]
                for opt in payload["data"].get("options", [])
            }
            if command_name in self.handlers:
                return await self.handlers[command_name](payload, **options)
        return {"type": 4, "data": {"content": "Unknown interaction type."}}
