import json
from datetime import datetime

def save_info(memes: list[str]) -> None:
    dic = {"memes": memes, "last_post_time": datetime.now().isoformat()}
    with open("appdata.json", "w") as f:
        f.write(json.dumps(dic, indent=4))

def load_info() -> dict | None:
    from os.path import exists
    if not exists("appdata.json"):
        return None

    with open("appdata.json", "r") as f:
        jsn = json.loads(f.read())
        jsn["last_post_time"] = datetime.fromisoformat(jsn["last_post_time"])
        return jsn
