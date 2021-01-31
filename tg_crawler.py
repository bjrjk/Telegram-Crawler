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

def initChats(tg):
    offset_chat_id = 0
    chat_ids = []
    offset_order = 2 ** 63 - 1
    chats_received = True

    while chats_received:
        result = tg.get_chats(offset_order=offset_order, offset_chat_id=offset_chat_id)
        result.wait()

        if result.update['chat_ids']:
            pprint(result.update)
            chat_ids += result.update['chat_ids']
            chat_info = tg.get_chat(chat_ids[-1])
            chat_info.wait()
            offset_chat_id = chat_info.update['id']
            offset_order = chat_info.update['order']
        else:  # no more chats to load
            chats_received = False

    print('Chats: ', chat_ids)

def main():
    try:
        tg = init()
        initChats(tg)
        #result = tg.get_me()
        #result.wait()
        #pprint(result.update)

    finally:
        uninit(tg)


if __name__ == '__main__':
    main()
