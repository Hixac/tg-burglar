from config import TG_API_ID, TG_API_HASH, TG_PHONE
from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel

client = TelegramClient('rofls', TG_API_ID, TG_API_HASH)
client.start(phone=TG_PHONE)

class Channel:
    @property
    def do_not_name(self) -> bool:
        return self._do_not_name

    @property
    def score(self) -> int:
        return self._score

    @property
    def name(self) -> str:
        return self._identifier

    def __init__(self, identifier: str | int, score: int = 0, do_not_name: bool = False):
        self._score = score
        self._do_not_name = do_not_name
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

    def inc_score(self):
        self._score += 1

    def to_dict(self):
        return {"score": self._score, "do_not_name": self._do_not_name}
