# -*- coding: utf-8 -*-
import aiohttp
from aiohttp.web_response import Response

from config import BotConfig

session = aiohttp.ClientSession()


async def query_char(char: str):
    async with session.get(BotConfig.XHUP_CHARS_QUERY_API, json={"char": char}) as resp:
        if resp.status == 404:
            return f"{char}：未收录该字"
        res = await resp.json()
        return res['info'].rstrip().replace("=", '\n  ')
