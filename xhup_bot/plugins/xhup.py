

"""
待实现
"""
from aiocqhttp import CQHttp
from aiocqhttp.message import Message
from typing import Dict, Any

from config import BotConfig
from xhup_bot import on_group_command, on_private_command, xhup_club


@on_group_command(r"[?？](?P<char>\w)", at_me=False)
@on_private_command(r"[?？]?(?P<char>\w)")
async def query_char(bot: CQHttp, context: Dict[str, Any], groupdict):
    """拆字"""
    char = groupdict['char']
    if char not in BotConfig.SYMBOLS_ALL:  # 剔除标点
        info = await xhup_club.query_char(char)  # 查询拆字表
        if info:
            await bot.send(context, Message(info), at_sender=True)


# @on_group_command(r"[?？](?P<char>\w+)")
# @on_private_command(r"[?？]?(?P<char>\w+)")
# async def query_word(bot: CQHttp, context: Dict[str, Any], groupdict):
#     """查词库编码"""
#     pass


