from itertools import chain

import os
import string

from pathlib import Path

from dotenv import load_dotenv

from datetime import timedelta
from typing import Dict, Any

"""
加载配置
"""

# 1. 从 .env 加载配置

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class BotConfig(object):
    """
    NoneBot 配置
    """

    # 1. 来自 .env
    DEBUG = os.getenv("DEBUG")

    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")

    # 2. scheduler

    APSCHEDULER_CONFIG: Dict[str, Any] = {
        'apscheduler.timezone': 'Asia/Shanghai'
    }

    # 图灵聊天机器人 api
    turing_api = "http://openapi.tuling123.com/openapi/api/v2"
    TURING_KEY = os.getenv("TURING_KEY")

    # 短链api（范爷提供）
    SHORT_URL_API = os.getenv("SHORT_URL_API")
    SHORT_URL_TOKEN = os.getenv("SHORT_URL_TOKEN")

    # xhup-club-api
    XHUP_CLUB_API = os.getenv("XHUP_CLUB_API")
    XHUP_CLUB_TOKEN = os.getenv("XHUP_CLUB_TOKEN")

    # 字符相关
    SYMBOLS_US = frozenset(chain(string.printable, "  "))  # 也包含了数字和特殊标点
    SYMBOLS_CN = frozenset(r"！“,”#￥%&‘’（）*+，-。、：；《〈=〉》？@「、」…… ——`『|』~【】〖〗〔〕．〃＂……¨ˉ·─　")
    SYMBOLS_OTHER = frozenset(r"ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ０１２３４５６７８９")
    SYMBOLS_ALL = frozenset(chain(SYMBOLS_US, SYMBOLS_CN, SYMBOLS_OTHER))


def update_config(**kwargs):
    """
    TODO 通过 http-api 获取到各项 group_command 的权限
    通过 websocket，有修改时 xhup-http-api 就通知这边

    :param kwargs:
    :return:
    """
    for key, value in kwargs.items():
        setattr(BotConfig, key, value)
