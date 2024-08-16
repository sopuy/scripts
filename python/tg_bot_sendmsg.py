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
import requests

# optional
from pathlib import Path
import argparse
from dotenv import dotenv_values
import ast

logger = logging.getLogger(__name__)


def send_tg_msg_to_user(**kwargs):
    """
    send tg msg to user;
    Cannot be enabled webhook;
    The user needs to send a message to the bot first and obtain the chat id through the TG getUpdates interface;
    """

    chat_id = kwargs.get("chat_id")
    tg_token = kwargs.get("tg_token")
    content = kwargs.get("content", "hello world")
    https_proxy = kwargs.get("https_proxy", None)

    # tg sendmsg api
    # tg_bot_api_update = f"https://api.telegram.org/bot{tg_token}/getUpdates"
    tg_bot_api_send_msg = f"https://api.telegram.org/bot{tg_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": content,
    }
    # resp = requests.get(tg_bot_api_send_msg, params=payload)
    if https_proxy:
        resp = requests.post(tg_bot_api_send_msg, data=payload, proxies=https_proxy)
    else:
        resp = requests.post(tg_bot_api_send_msg, data=payload)
    logger.info(resp.text)
    return resp


def main():
    parser = argparse.ArgumentParser(description=PROG_DESC, add_help=True)
    parser.add_argument("-v", "--version", help="print version", action="version", version=PROG_VERSION)
    parser.add_argument("-e", "--env", help="set logger", default="dev")
    parser.add_argument("-id", type=int, help="The chat ID to send the message to")
    parser.add_argument("content", type=str, help="The content of the message")
    args = parser.parse_args()

    if args.env == "prod":
        handlers = [logging.FileHandler(f"{PROJECT_DIR}/logs/{PROG_NAME}.log", encoding="utf-8")]
    else:
        handlers = [logging.StreamHandler()]

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d] - %(message)s", handlers=handlers)

    # project dir
    PROJECT_DIR = Path(__file__).parent

    config = dotenv_values(f"{PROJECT_DIR}/tg.env")
    tg_token = config["PUSH_TOKEN"]
    chat_id = config["CHAT_ID"]
    # proxy
    if "PROXIES" in config:
        https_proxy = {"https": "http://localhost:32003"}
        # TODO: https proxy error - urllib3.exceptions.ProxySchemeUnsupported: TLS in TLS requires support for the 'ssl' module
        # proxy rules: https://urllib3.readthedocs.io/en/stable/advanced-usage.html
        # https_proxy = ast.literal_eval(config["PROXIES"])
        logger.info(f"send msg with proxy")
    else:
        https_proxy = None
        logger.info("send msg without proxy")

    if args.id:
        logger.info(f"send message to chat_id: {args.id}")
        send_tg_msg_to_user(chat_id=args.id, content=args.content, tg_token=tg_token, https_proxy=https_proxy)

    else:
        logger.info("use default chat_id")
        send_tg_msg_to_user(chat_id=chat_id, content=args.content, tg_token=tg_token, https_proxy=https_proxy)


if __name__ == "__main__":
    PROG_NAME = "tg_bot_sendmsg"
    PROG_VERSION = "0.0.1"
    PROG_DESC = "telegram bot api with sendMessage method;"
    main()
