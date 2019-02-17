from os import path

import nonebot

import config

"""
启动命令：`hypercorn run:app`
"""

nonebot.init(config.NoneBotConfig)
nonebot.load_plugins(
    path.join(path.dirname(__file__), 'xhup_bot', 'plugins'),
    'xhup_bot.plugins'
)
bot = nonebot.get_bot()
app = bot.asgi

if __name__ == '__main__':
    bot.run()

