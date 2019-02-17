from itertools import chain

import os
import string

from pathlib import Path

from dotenv import load_dotenv

from datetime import timedelta
from typing import Container, Union, Iterable, Pattern, Optional, Dict, Any

from nonebot.typing import Expression_T


"""
加载配置
"""

# 1. 从 .env 加载配置

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class NoneBotConfig(object):
    """
    NoneBot 配置
    """

    # 1. 来自 .env
    DEBUG = os.getenv("DEBUG")

    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    SECRET = os.getenv("SECRET")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")

    # 2. 其它

    SUPERUSERS: Container[int] = {1643147099, }
    NICKNAME: Union[str, Iterable[str]] = ''
    COMMAND_START: Iterable[Union[str, Pattern]] = {'/', '!', '／', '！'}
    COMMAND_SEP: Iterable[Union[str, Pattern]] = {'/', '.'}
    SESSION_EXPIRE_TIMEOUT: Optional[timedelta] = timedelta(minutes=5)
    SESSION_RUN_TIMEOUT: Optional[timedelta] = None
    SESSION_RUNNING_EXPRESSION: Expression_T = '您有命令正在执行，请稍后再试'
    SHORT_MESSAGE_MAX_LENGTH: int = 50
    DEFAULT_VALIDATION_FAILURE_EXPRESSION: Expression_T = '您的输入不符合要求，请重新输入'

    APSCHEDULER_CONFIG: Dict[str, Any] = {
        'apscheduler.timezone': 'Asia/Shanghai'
    }


class XhupBotConfig(object):
    """
    xhup_bot 的配置
    """

    # 图灵聊天机器人 api
    turing_api = "http://openapi.tuling123.com/openapi/api/v2"
    turing_key = os.getenv("TURING_KEY")

    # 短链api（范爷提供）
    short_url_api = os.getenv("SHORT_URL_API")
    short_url_token = os.getenv("SHORT_URL_TOKEN")

    # xhup-club-api
    xhup_club_api = os.getenv("XHUP_CLUB_API")
    xhup_club_token = os.getenv("XHUP_CLUB_TOKEN")

    # 字符相关
    symbols_us = string.printable  # 也包含了数字和特殊标点
    symbols_cn = r"！“,”#￥%&‘,’（）*+，-。、：；《〈=〉》？@「、」…… " \
                 r"——`『|』~【】〖〗〔〕．〃＂、……¨ˉ·"
    symbols_all = frozenset(chain(symbols_us, symbols_cn))

