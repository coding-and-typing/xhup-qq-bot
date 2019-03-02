# -*- coding: utf-8 -*-
import logging

from aiocqhttp import CQHttp
from aiocqhttp.message import Message
from typing import Dict, Any

from config import BotConfig
import xhup_qq_bot
from xhup_qq_bot.command import handle_group_message, handle_private_message

"""
启动命令：`hypercorn run:app`
"""

logger = logging.getLogger("xhup-qq-bot")

bot = CQHttp(access_token=BotConfig.ACCESS_TOKEN,
             message_class=Message,
             enable_http_post=False)


@bot.on_message("group")
async def handle(context: Dict[str, Any]):
    """群聊"""
    await handle_group_message(bot, context)


@bot.on_message("private")
async def handle(context: Dict[str, Any]):
    """私聊"""
    await handle_private_message(bot, context)


# app = bot.server_app

# @app.route('/groups_permission')
# async def groups_permission():
#     """提供群权限上报 api"""
#     pass

if __name__ == '__main__':
    xhup_qq_bot.load_builtin_plugins()  # 加载插件
    bot.run(host=BotConfig.HOST, port=BotConfig.PORT)
