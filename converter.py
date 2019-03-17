# -*- coding: utf-8 -*-

"""
进行 xhup-club-api 与 cqhttp 之间的消息转换
"""

update_format = {
    "platform": 'qq',  # or 'telegram'、'wechat'
    "type": "message",  # or 'notice'
    "message": {  # 如果 update 类型是 message
        "type": "private",  # or 'group'
        "user": {
            "id": "",  # 用户 id，QQ 号等
            "role": "owner",  # 群组 owner/admin/other
        },
        "group": {
            "id": "",  # 群 id
            "at_me": True,  # 是否是 at 我
        },

        "text": "",  # 消息的 text 部分。（去除掉了表情、at 和多媒体数据）
        "photo": "",  # 图片路径
    },
    "notice": {  # 如果 update 类型是 notice 的话
        # TODO 暂时未实现
    }
}


def cq_2_xhup(info):
    """
    将 cqhttp 消息转换成 xhup 需要的格式
    :param info:
    :return:
    """

    return info


def xhup_2_cq(info):
    """
    将 xhup 消息转换成 cqhttp 需要的格式
    :param info:
    :return:
    """

    return info
