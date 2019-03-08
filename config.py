from itertools import chain

import logging
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
    DEBUG = True if os.getenv("DEBUG") == 'True' else False
    LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")

    NICKNAME = "拆小鹤"

    # xhup-club-api
    XHUP_CLUB_API = os.getenv("XHUP_CLUB_API")
    XHUP_CLUB_TOKEN = os.getenv("XHUP_CLUB_TOKEN")


