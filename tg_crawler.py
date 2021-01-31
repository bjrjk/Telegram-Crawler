import argparse

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
        chat_id: int,
        limit: int = 100,
        from_message_id: int = 0
):
    pass

def retreive_messages(telegram, chat_id, receive_limit):
    receive = True
    from_message_id = 0
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
                stats_data[message['id']] = message['content']['text']['text']
            from_message_id = message['id']

        total_messages = len(stats_data)
        if total_messages > receive_limit or not response.update['total_count']:
            receive = False

        print(f'[{total_messages}/{receive_limit}] received')

    return stats_data

def main():
    try:
        tg = init()
        chatsList = initChatsList(tg)
        groupTitle = '𝗦𝗜𝗚𝗞𝗜𝗦𝗦💋'
        chatID = getChatIDByTitle(chatsList, groupTitle)
        print(retreive_messages(tg, chatID, 100))

        #chatHistory = tg.get_chat_history(chat_id=chatID, limit=50, from_message_id=0, offset=0, only_local=False)
        #chatHistory.wait()
        #pprint(chatHistory.error_info)
        #pprint(chatHistory.update)
    finally:
        uninit(tg)


if __name__ == '__main__':
    main()
