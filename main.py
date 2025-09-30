import vk_api
import my_tg
from my_tg import Error
import my_json
from eprint import eprint
from datetime import datetime
from time import sleep
from config import GROUP_ID, USER_TOKEN

session = vk_api.VkApi(token=USER_TOKEN)

def wall_post(msg: str, attachments: str) -> None:
    session.method("wall.post", {"owner_id": GROUP_ID, "message": msg, "attachments": attachments, \
                   "publish_date": datetime.now().timestamp() + 60 * 60 * 2})

def get_upload_video(direc: str, msg: str) -> str:
    upload = vk_api.VkUpload(session)
    temp = upload.video(direc, group_id=-GROUP_ID, wallpost=True, description=msg)

    return "video" + str(temp["owner_id"]) + "_" + str(temp["video_id"])

def get_upload_photo(direc: str | list[str]) -> str:
    upload = vk_api.VkUpload(session)
    temp = upload.photo_wall(direc, group_id=-GROUP_ID)

    ret = []
    for photo in temp:
        ret.append("photo" + str(photo["owner_id"]) + "_" + str(photo["id"]))

    return ",".join(ret)

def pause(info: dict | None) -> None:
    if info is not None:
        last_time = info["last_post_time"]

        period = 60 * 60 # 1 hour
        time_diff = (datetime.now() - last_time).total_seconds()
        eprint("Time left to post " + str(time_diff))
        sleep(period - time_diff if period - time_diff > 0 else 0)

while True:

    info = my_json.load_info()
    pause(info)
    if info is None:
        info = {'memes': []}

    try:
        media = my_tg.channel_new_post(info["memes"])
        match media:
            case Error.SAME_POST:
                eprint("same_post")
            case _:
                wall_post(f"Источник: тгк \"{media['channel_name']}\"", get_upload_photo(media['files']))
                info['memes'].extend(media["files"])
                my_json.save_info(info['memes'], [chn.name for chn in my_tg.get_channels()])
    except Exception as e:
        import traceback
        eprint(f"Ошибка обработки команды: {e}")
        eprint(traceback.format_exc() + '\n')
