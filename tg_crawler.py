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

def main():
    try:
        tg = init()

        result = tg.get_me()
        result.wait()
        pprint(result.update)

    finally:
        uninit(tg)


if __name__ == '__main__':
    main()
