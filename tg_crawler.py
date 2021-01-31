import argparse,time,json

from pprint import pprint
from telegram.client import Telegram

import utils

def init():
    utils.setup_logging()

    parser = argparse.ArgumentParser()
    utils.add_api_args(parser)
    utils.add_proxy_args(parser)
    args = parser.parse_args()

    tg = Telegram(
        api_id=args.api_id,
        api_hash=args.api_hash,
        phone=args.phone,
        database_encryption_key=args.db_key,
        proxy_server=args.proxy_server,
        proxy_port=args.proxy_port,
        proxy_type=utils.parse_proxy_type(args)
    )
    tg.login()

    return tg

def uninit(tg):
    tg.stop()

def initChatsList(tg):
    offset_chat_id = 0
    chatsList = {}
    offset_order = 2 ** 63 - 1
    chats_received = True

    while chats_received:
        result = tg.get_chats(offset_order=offset_order, offset_chat_id=offset_chat_id)
        result.wait()
        chatsDict = result.update['chat_ids']
        if chatsDict:
            for chatID in chatsDict:
                chat_info = tg.get_chat(chatID)
                chat_info.wait()
                title = chat_info.update['title']
                chatsList[title] = chatID
            chat_info = tg.get_chat(chatsDict[-1])
            chat_info.wait()
            offset_chat_id = chat_info.update['id']
            offset_order = chat_info.update['positions'][0]['order']
        else:
            chats_received = False

    return chatsList

def getChatIDByTitle(chatsList, title):
    for key, value in chatsList.items():
        if key.find(title) != -1:
            return value
    return None

def getChatMessage(
        telegram,
        chat_id: int,
        receive_limit: int = -1,
        from_message_id: int = 0,
        sleep_interval: float = 1
):
    receive = True
    stats_data = {}

    while receive:
        response = telegram.get_chat_history(
            chat_id=chat_id,
            limit=1000,
            from_message_id=from_message_id,
        )
        response.wait()
        for message in response.update['messages']:
            if message['content']['@type'] == 'messageText':
                stats_data[message['id']] = {
                    "text": message['content']['text']['text'],
                    "date": message['date'],
                    "sender_user_id": message['sender']['user_id']
                }
            from_message_id = message['id']
        total_messages = len(stats_data)
        if (receive_limit != -1 and total_messages > receive_limit) or not response.update['total_count']:
            receive = False
        print(f'[{total_messages}/{receive_limit}] received')
        time.sleep(sleep_interval)

    return stats_data

def main():
    try:
        tg = init()
        chatsList = initChatsList(tg)
        groupTitle = '𝗦𝗜𝗚𝗞𝗜𝗦𝗦💋'
        chatID = getChatIDByTitle(chatsList, groupTitle)
        messageData = getChatMessage(telegram = tg, chat_id = chatID, receive_limit = 1000)
        utils.WriteTXT('chatMessages.log', json.dumps(messageData))
    finally:
        uninit(tg)


if __name__ == '__main__':
    main()
