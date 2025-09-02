import vk_api
import tg
import my_json
from datetime import datetime
from time import sleep
from config import GROUP_ID, USER_TOKEN

session = vk_api.VkApi(token=USER_TOKEN)

def wall_post(msg: str, attachments: str) -> None:
    session.method("wall.post", {"owner_id": GROUP_ID, "message": msg, "attachments": attachments})

def get_upload_video(direc: str, msg: str) -> str:
    upload = vk_api.VkUpload(session)
    temp = upload.video(direc, group_id=-GROUP_ID, wallpost=True, description=msg)

    return "video" + str(temp["owner_id"]) + "_" + str(temp["video_id"])

def get_upload_photo(direc: str | list[str]) -> list[str]:
    upload = vk_api.VkUpload(session)
    temp = upload.photo_wall(direc, group_id=-GROUP_ID)

    ret = []
    for photo in temp:
        ret.append("photo" + str(photo["owner_id"]) + "_" + str(photo["id"]))

    return ret

def log(msg: str) -> None:
    with open("log.log", "a") as f:
        f.write(msg + "\n")

memes = []
while True:
    
    info = my_json.load_info()
    if info is not None:
        memes = info["memes"]

        last_time = info["last_post_time"]

        period = 60 # minutes
        period *= 60 # to seconds
        time_diff = (datetime.now() - last_time).total_seconds()
        log("Time left to post " + str(time_diff))
        sleep(period - time_diff if period - time_diff > 0 else 0)

    try:
        channel = tg.channel_new_post()
        files = [i[0] for i in channel["post"]]
        log(str(channel))
        if any([i[1].isoformat() + f"_{channel['channel_name']}" in memes for i in channel["post"]]):
            log("fall asleep")
            sleep(60 * 60 * 24) # 24 hours pause
            continue
        if ".mp4" in files[0].lower():
            get_upload_video(files[0], f"Источник: тгк \"{channel['channel_name']}\"")
        else:
            post = ",".join(get_upload_photo(files))
            wall_post(f"Источник: тгк \"{channel['channel_name']}\"", post)
    except Exception as e:
        import traceback
        log(f"Ошибка обработки команды: {e}")
        log(traceback.format_exc() + '\n')
        continue

    memes.extend([i[1].isoformat() + f"_{channel['channel_name']}" for i in channel["post"]])
    my_json.save_info(memes)
    tg.export_score()
