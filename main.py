import vk_api
import my_tg
import my_json
from eprint import eprint
from datetime import datetime
from time import sleep
from config import GROUP_ID, USER_TOKEN

session = vk_api.VkApi(token=USER_TOKEN)

def wall_post(msg: str, attachments: str) -> None:
    session.method("wall.post", {"owner_id": GROUP_ID, "message": msg, "attachments": attachments, \
                   "publish_date": datetime.now().timestamp() + 60 * 60 * 8})

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

def pause(last_time: datetime) -> None:
    period = 60 * 60 # 1 hour
    time_diff = (datetime.now() - last_time).total_seconds()
    eprint("Time left to post " + str(time_diff))
    sleep(period - time_diff if period - time_diff > 0 else 0)

while True:

    pause(my_json.get_time())

    try:
        media = my_json.channel_new_post()
        match media:
            case my_json.Error.SAME_POST:
                eprint("same_post")
            case _:
                channel = media["channel"]

                description = "" if channel.do_not_name else f"Источник: тгк \"{channel.name}\""
                wall_post(description, get_upload_photo(media['files']))
                my_json.write(media["files"], channel)

    except Exception as e:
        import traceback
        eprint(f"Ошибка обработки команды: {e}")
        eprint(traceback.format_exc() + '\n')
