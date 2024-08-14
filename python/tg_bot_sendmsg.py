#!/usr/bin/env python3
# coding=utf-8
###############################################################################
"""
__author__ = "Daning"

Description:
    telegram bot api with sendMessage method;
    Cannot be enabled webhook;
    The user needs to send a message to the bot first and obtain the chat id through the TG getUpdates interface;
"""

import logging
from pathlib import Path
from dotenv import dotenv_values

# project dir
PROJECT_DIR = Path(__file__).parent

logger = logging.getLogger(__name__)

config = dotenv_values(f"{PROJECT_DIR}/tg.env")
tg_token = config["PUSH_TOKEN"]
chatID = config["CHAT_ID"]

# tg sendmsg api
tg_bot_api_update = f"https://api.telegram.org/bot{tg_token}/getUpdates"
tg_bot_api_send_msg = f"https://api.telegram.org/bot{tg_token}/sendMessage"


def send_tg_msg_to_user(**kwargs):
    """
    send tg msg to user;
    Cannot be enabled webhook;
    The user needs to send a message to the bot first and obtain the chat id through the TG getUpdates interface;
    """
    import requests

    chat_id = kwargs.get("chat_id", chatID)
    content = kwargs.get("content", "hello world")
    payload = {
        "chat_id": chat_id,
        "text": content,
    }
    # resp = requests.get(tg_bot_api_send_msg, params=payload)
    resp = requests.post(tg_bot_api_send_msg, data=payload)
    logger.info(resp.text)
    return resp


def main():
    import argparse

    parser = argparse.ArgumentParser(description=PROG_DESC, add_help=True)
    parser.add_argument("-v", "--version", help="print version", action="version", version=PROG_VERSION)
    parser.add_argument("-e", "--env", help="set logger", default="dev")
    parser.add_argument("-id", type=int, help="The chat ID to send the message to")
    parser.add_argument("content", type=str, help="The content of the message")
    args = parser.parse_args()

    if args.env == "prod":
        from pathlib import Path

        PROJECT_DIR = Path(__file__).parent
        handlers = [logging.FileHandler(f"{PROJECT_DIR}/logs/{PROG_NAME}.log", encoding="utf-8")]
    else:
        handlers = [logging.StreamHandler()]

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d] - %(message)s", handlers=handlers)

    if args.id:
        logger.info(f"send message to chat_id: {args.id}")
        send_tg_msg_to_user(chat_id=args.id, content=args.content)

    else:
        logger.info("use default chat_id")
        if args.content:
            send_tg_msg_to_user(content=args.content)
        else:
            logger.error("no content, exit scripts...")


if __name__ == "__main__":
    PROG_NAME = "tg_bot_sendmsg"
    PROG_VERSION = "0.0.1"
    PROG_DESC = "telegram bot api with sendMessage method;"
    main()
