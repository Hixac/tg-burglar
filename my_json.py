import os

import json
from enum import Enum
from eprint import eprint
from my_tg import Channel
from datetime import datetime

channels: list[Channel] = [Channel("neblagUwUdnaya"), Channel("tulpsred"), Channel("milkopechenegi"),\
         Channel("crabmodern"), Channel("me_mbl"), \
         Channel("progsiveexp"), Channel("ragtg"), Channel("hotbebranakedstars"), Channel("durtmk"), \
         Channel("Current_memes"), Channel("memesjuice"), Channel("itvbia"), Channel("bredoq"), \
         Channel("spazm_aticus", do_not_name=True), Channel("zakrest", do_not_name=True), \
         Channel("UltRandShitt"), Channel("SBUNEM"), Channel("schizoracing"), Channel("beobanka", do_not_name=True), \
         Channel("click_for_death"), Channel("shizopathia")]

def load() -> dict:
    with open("appdata.json", "r") as f:
        jsn = json.loads(f.read())
        jsn["last_post_time"] = datetime.fromisoformat(jsn["last_post_time"])
        return jsn

def save(info: dict) -> None:
    # info contains {"channels", "memes", "last_post_time"}
    info["last_post_time"] = datetime.now().isoformat()
    with open("appdata.json", "w") as f:
        f.write(json.dumps(info, indent=4))

# BEHOLD IT IS SHITCODE

if not os.path.exists("appdata.json"):
    with open("appdata.json", "w") as f:
        f.write(json.dumps({"memes": [], "last_post_time": datetime.now().isoformat(), "channels": {}}, indent=4))

info = load()
for chn in channels:
    if chn.name not in info["channels"]:
        info["channels"][chn.name] = chn.to_dict()
save(info)

def write(memes: list[str], channel: Channel):
    info = load()
    info["memes"].extend(memes)
    info["channels"][channel.name] = {"score": channel.score, "do_not_name": channel.do_not_name}
    save(info)

def get_channel(name: str) -> dict:
    info = load()
    return {"score": info[name]["score"], "do_not_name": info[name]["do_not_name"]}

def get_time() -> datetime:
    return load()["last_post_time"]

def get_memes() -> list[str]:
    return load()["memes"]

class Error(Enum):
    SAME_POST = 0

chn_idx = 0
def channel_new_post() -> dict | Error:
    global chn_idx

    channel = channels[chn_idx % len(channels)]
    chn_idx += 1

    media = channel.get_newest_post()
    for file in media:
        if file in get_memes():
            return Error.SAME_POST
    channel.inc_score()

    eprint(channels)
    eprint(media)
    return {"files": media, "channel": channel}

def get_channels() -> list:
    return channels
