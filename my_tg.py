import my_json
from enum import Enum
from eprint import eprint
from config import TG_API_ID, TG_API_HASH, TG_PHONE
from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel

Filename = str

client = TelegramClient('rofls', TG_API_ID, TG_API_HASH)
client.start(phone=TG_PHONE)

class Channel:
    @property
    def name(self) -> str:
        return self._identifier

    def __init__(self, identifier: str | int):
        if isinstance(identifier, int):
            self._identifier = PeerChannel(identifier)
        else:
            self._identifier = identifier

    def get_newest_post(self) -> list:
        for msg in client.iter_messages(self._identifier, limit=100):
            if not msg.fwd_from and msg.photo is not None:
                message = msg
                break

        if message.grouped_id is not None:
            search_ids = [i for i in range(message.id - 10, message.id + 10 + 1)]
            posts = client.get_messages(self._identifier, ids=search_ids)
            media = []
            for post in posts:
                if post is not None and post.grouped_id == message.grouped_id and post.photo is not None:
                    media.append(post.download_media(file=post.date + f"_{self._identifier}.jpg"))
            return media

        return [message.download_media(file=message.date.isoformat() + f"_{self._identifier}.jpg")]

channels: list[Channel] = [Channel("neblagUwUdnaya"), Channel("tulpsred"), Channel("milkopechenegi"),\
         Channel("crabmodern"), Channel("me_mbl"), \
         Channel("progsiveexp"), Channel("ragtg"), Channel("hotbebranakedstars"), Channel("durtmk"), \
         Channel("Current_memes"), Channel("memesjuice"), Channel("itvbia"), Channel("bredoq"), \
         Channel("spazm_aticus")]

def load():
    global chn_idx, channels

    g_info = my_json.load_info()
    if g_info is not None:
        channels.clear()
        for name in g_info['channels']:
            channels.append(Channel(name))
load()

class Error(Enum):
    SAME_POST = 0

chn_idx = 0
def channel_new_post(memes: list) -> dict | Error:
    global chn_idx

    channel = channels[chn_idx % len(channels)]
    chn_idx += 1

    media = channel.get_newest_post()
    for file in media:
        if file in memes:
            return Error.SAME_POST

    eprint(channels)
    eprint(media)
    return {"files": media, "channel_name": channel.name}

def get_channels() -> list:
    return channels
