from aiocqhttp import CQHttp
from aiocqhttp.message import Message
from typing import Dict, Any

from config import BotConfig
from xhup_qq_bot import on_group_command, on_private_command, xhup_club


@on_group_command(r"[?？]群绑定 (?P<code>[a-zA-Z0-9]{6})", at_me=False)
async def query_char(bot: CQHttp, context: Dict[str, Any], groupdict):
    """拆字"""
    code = groupdict['code']
    # 上报到 xhup-http-api




