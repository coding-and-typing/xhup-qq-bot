# -*- coding: utf-8 -*-
import asyncio

import json
import logging
import websockets

from aiocqhttp import CQHttp
from aiocqhttp.message import Message
from typing import Dict, Any, Optional

from config import BotConfig
from converter import cq_2_xhup, xhup_2_cq

logging.basicConfig(level=BotConfig.LOG_LEVEL)

"""
启动命令：`hypercorn run:app`
"""

logger = logging.getLogger("xhup-qq-bot")

bot = CQHttp(access_token=BotConfig.ACCESS_TOKEN,
             message_class=Message,
             enable_http_post=False)

xhup_club_ws = None


async def get_xhup_club_ws():
    """连接 xhup_club_api，不断重试直到连上为止"""
    global xhup_club_ws

    while True:  # 如果连接失败，永远重试
        connect = websockets.connect(BotConfig.XHUP_CLUB_API,
                                     extra_headers={
                                         "Authorization": f"Token {BotConfig.XHUP_CLUB_TOKEN}"
                                     })
        try:
            xhup_club_ws = await connect
            logger.debug("后端连接成功")
            return xhup_club_ws
        except OSError as e:
            logger.info(e)
            logger.info("后端连接失败，三秒后重连")
            await asyncio.sleep(3)


async def handle_xhup_club_event():
    """
    在收到 xhup 发过来的消息时，将它处理后转发给 CoolQ
    """
    global xhup_club_ws
    while True:  # 这个是一个 run_forever 的 task
        if xhup_club_ws:
            try:
                reply = json.loads(await xhup_club_ws.recv())
                if reply:
                    cq_reply = xhup_2_cq(reply)
                    logger.debug(f"机器人回复消息：{cq_reply}")
                    await bot.send_msg(**cq_reply)
            except websockets.ConnectionClosed as e:
                logger.info(e)
                logger.info("后端连接断开，三秒后自动重连")
                await asyncio.sleep(3)
                xhup_club_ws = await get_xhup_club_ws()
            except Exception as e:
                logger.warning(e)
        else:
            logger.info("后端尚未连接，现在尝试连接。")
            xhup_club_ws = await get_xhup_club_ws()


@bot.on_message()
async def handle_msg(context):
    """
    在收到 CoolQ 消息时，将消息处理后，转发给 xhup
    """
    logger.debug(f"收到消息：{context}")

    global xhup_club_ws
    if xhup_club_ws:
        try:
            xhup_msg = cq_2_xhup(context)
            await xhup_club_ws.send(json.dumps(xhup_msg))
        except websockets.ConnectionClosed as e:
            logger.info(e)
            logger.info("后端连接断开，三秒后自动重连")
            await asyncio.sleep(3)
            xhup_club_ws = await get_xhup_club_ws()
    else:
        logger.info("后端尚未连接，现在尝试连接。")
        xhup_club_ws = await get_xhup_club_ws()


# @bot.on_notice('group_increase')
# async def handle_group_increase(context):
#     await bot.send(context, message='欢迎新人～',
#                    at_sender=True, auto_escape=True)


if __name__ == '__main__':
    # obtain the event loop from asyncio
    loop = asyncio.get_event_loop()

    # 先连接上 xhup-club-api 后端
    loop.run_until_complete(get_xhup_club_ws())

    # 后台跑这个任务，将 xhup 消息转发给 CoolQ
    loop.create_task(handle_xhup_club_event())

    # 启动 aiocqhttp
    bot.run(host=BotConfig.HOST, port=BotConfig.PORT)
