import json
from config import TG_API_ID, TG_API_HASH, TG_PHONE
from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel

Filename = str

client = TelegramClient('rofls', TG_API_ID, TG_API_HASH)
client.start(phone=TG_PHONE)

class Channel:
    @property
    def score(self) -> int:
        return self._score

    @property
    def name(self) -> str:
        return self._identifier

    def __init__(self, identifier: str | int, score: int = 0):
        self._score: int = score # to not post same channel
        if isinstance(identifier, int):
            self._identifier = PeerChannel(identifier)
        else:
            self._identifier = identifier

    def get_newest_post(self) -> list[tuple]: # tuple ( filename, datetime )
        self._score += 1

        for msg in client.iter_messages(self._identifier, limit=100):
            if msg.photo is not None or msg.video is not None:
                message = msg
                break

        if message.grouped_id is not None:
            search_ids = [i for i in range(message.id - 10, message.id + 10 + 1)]
            posts = client.get_messages(self._identifier, ids=search_ids)
            media = []
            for post in posts:
                if post is not None and post.grouped_id == message.grouped_id and post.photo is not None:
                    media.append((post.download_media(), post.date))
            return media

        return [(client.download_media(message.media), message.date)]

def export_score() -> None:
    d = {}
    for i in channels:
        d[i.name] = i.score
    
    with open("exported_info.json", "w") as f:
        f.write(json.dumps(d, indent=4))

def import_score() -> None:
    from os.path import exists
    if not exists("exported_info.json"):
        return

    d = {}
    with open("exported_info.json", "r") as f:
        d = json.loads(f.read())

    global channels
    channels = [Channel(key, int(val)) for key, val in d.items()]

channels: list[Channel] = [Channel("neblagUwUdnaya"), Channel("larkovoe"), \
        Channel("tulpsred"), Channel("milkopechenegi"), Channel("crabmodern"), Channel("me_mbl"), \
        Channel("progsiveexp"), Channel("ragtg"), Channel("hotbebranakedstars"), Channel("durtmk"), \
        Channel("Current_memes"), Channel("memesjuice"), Channel("itvbia"), Channel("bredoq"), \
        Channel("spazm_aticus")]

import_score()

def channel_new_post() -> dict:
    l = sorted(channels, key=lambda ch: ch.score)
    return {"post": l[0].get_newest_post(), "channel_name": l[0].name}

