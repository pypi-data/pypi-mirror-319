from .embed import Embed

def send_message(content: str = None, embed: Embed = None, ephemeral: bool = False):
    data = {}
    if content:
        data["content"] = content
    if embed:
        data["embeds"] = [embed.to_dict()]
    if ephemeral:
        data["flags"] = 64

    return {
        "type": 4,
        "data": data
    }
