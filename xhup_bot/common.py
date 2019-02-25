import aiohttp
import json

from config import BotConfig

session = aiohttp.ClientSession()


async def talk(message: str, user_id, group_id=None, username=None):
    """图灵机器人服务"""
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": message
            }
        },
        "userInfo": {
            "apiKey": BotConfig.TURING_KEY,
            "userId": user_id,
            "groupId": group_id,
            "userIdName": username,
        }
    }

    async with session.post(BotConfig.TURING_API, json=data) as resp:
        await resp.json()
        resp_json = json.loads(await resp.text())  # MD，还得手动转。。

    # 分析返回值
    code = resp_json['intent']["code"]
    if code < 10000:  # 异常
        return "异常状况，即将崩坏。9 8 7..."

    codes_text_only = [  # 可以直接输出的 code
        10004,  # 聊天
        10008,  # 天气
        10009,  # 计算
        10010,  # 故事
        10011,  # 成语接龙
        10013,  # 百科
        10016,  # 快递查询
        10019,  # 日期
        10020,  # 翻译
        10022,  # 脑筋急转弯
        10030,  # 歇后语
        10031,  # 绕口令
        10032,  # 顺口溜
        10033,  # 邮编
        10034,  # 自定义语料库
        10041,  # 星座运势（包含多个）
    ]
    if code in codes_text_only:  # 可以直接输出
        return resp_json['results'][0]["values"]['text']

    return "暂不提供该功能"
