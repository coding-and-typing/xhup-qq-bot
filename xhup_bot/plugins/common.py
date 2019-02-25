# -*- coding: utf-8 -*-
from aiocqhttp import CQHttp
from aiocqhttp.message import Message
from typing import Dict, Any

from config import BotConfig
from xhup_bot import on_group_command, on_private_command, xhup_club
from xhup_bot.common import talk


@on_group_command(".*", at_me=True)
@on_private_command("[:：].*")
async def talk_(bot: CQHttp, context: Dict[str, Any], groupdict):
    """聊天"""
    resp = await talk(context['message'].extract_plain_text(),
                      user_id=context['user_id'],
                      group_id=context.get('group_id'),
                      username=context['sender']['nickname'])
    await bot.send(context, Message(resp), at_sender=True)

