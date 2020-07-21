from queue import Queue
import requests
import threading
import Classes
import settings
import time


def telegramSpoof():
    print("TG Started")
    tg = Classes.TelegramChecker(settings.telegram_bot_token)
    offset = 0
    while True:
        update = tg.getUpdates(timeout=50, allowed_updates=["message"], offset=offset)
        for res in update['result']:
            if "message" in res.keys():
                message = 'message'
            else:
                message = 'edited_message'
            if "forward_from" in res[message].keys():
                continue
            chat_id = res[message]['chat']['id']
            if chat_id != -448429865:
                continue
            user_id = res[message]['from']['id']
            date = res[message]['date']
            if "text" not in res[message].keys():
                continue
            text = res[message]['text']
            offset = res['update_id'] + 1
            data = ["TG", user_id, text, date]
            q.put(refactor(data))


def vkSpoof():
    print("VK Started")
    vk = Classes.VkChecker()
    while True:
        update = vk.getUpdates()
        for updates in update['updates']:
            update_id = updates[0]
            if update_id != 4:
                continue
            peer_id = updates[3]
            if peer_id != 2000000093:
                continue
            date = updates[4]
            text = updates[5]
            if text == '':
                continue
            user_id = updates[6]['from']
            data = ["VK", user_id, text, date]
            q.put(refactor(data))


def refactor(data):  # {VK or TG} {user_id} {text} {time}
    try:
        if data[0] == "TG":
            name = settings.tg_table[data[1]]
        else:
            name = settings.vk_table[data[1]]
    except:
        name = "Unknown"
        print(f"  Warning: user {data[1]} in {data[0]} unknown!!! ")
    avatar = settings.avatars[name]
    return [name, data[2], data[3], avatar]  # [{name}, {text}, {time}]


def discordSender():
    while True:
        message = q.get()
        url = settings.discord_webhook
        text = f"{message[1]}\n" \
               f"||{time.ctime(message[2])}||"
        r = requests.post(url, json={'content': text, 'username': message[0], 'avatar_url': message[3]})

        print(f"{message[0]} {message[1]} {message[2]}")


if __name__ == "__main__":
    # new thread telegramSpoof
    # new thread vkSpoof
    # create threadsafety queue
    # start discordSender
    q = Queue()

    threading.Thread(target=telegramSpoof, daemon=True).start()
    threading.Thread(target=vkSpoof, daemon=True).start()

    discordSender()
