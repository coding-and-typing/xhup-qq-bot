from itertools import chain

import logging
import os
import string

from pathlib import Path

from datetime import timedelta
from typing import Dict, Any

"""
加载配置
"""


class BotConfig(object):
    """
    NoneBot 配置
    """

    # 1. 来自 .env
    DEBUG = os.getenv("DEBUG") == 'True'
    LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    HOST = os.getenv("HOST", "xhup-qq-bot")  # 容器间通过 dns 互访
    PORT = int(os.getenv("PORT", 8080))

    NICKNAME = "拆小鹤"

    # xhup-club-api
    XHUP_CLUB_API = os.getenv("XHUP_CLUB_API")
    XHUP_CLUB_TOKEN = os.getenv("XHUP_CLUB_TOKEN")


