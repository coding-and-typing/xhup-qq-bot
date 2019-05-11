# -*- coding: utf-8 -*-

"""
进行 xhup-club-api 与 cqhttp 之间的消息转换
"""
from aiocqhttp.message import Message, MessageSegment

from config import BotConfig


def is_at_me(msg, self_id):
    self_id = int(self_id)
    for item in msg:
        if item['type'] == 'at' \
                and int(item['data']['qq']) == self_id:
            return True
        elif item['type'] == 'text' \
                and BotConfig.NICKNAME in item['data']['text']:
            return True

    return False


def extract_images(msg):
    res = []
    for item in msg:
        if item['type'] == 'image':
            img = item['data']
            res.append({
                "filename": img['file'],
                "url": img['url'],
            })

    return res


def cq_2_xhup(info):
    """
    将 cqhttp 消息转换成 xhup 需要的格式
    :param info:
    :return:
    """
    res = {
        "platform": 'qq',
        "type": info['post_type'],
    }

    if res['type'] == "message":
        return {
            **res,
            "message": {  # 如果 update 类型是 message
                "type": info.get("message_type"),  # 'private' or 'group'
                "user": {
                    "id": info.get('user_id'),  # 用户 id，QQ 号等
                    "nickname": info['sender'].get('nickname'),
                    "role": info['sender'].get('role'),  # 群组 owner/admin/other，非群组消息时，它为 None
                },
                "group": {
                    "id": info['group_id'],  # 群 id
                    "at_me": is_at_me(info['message'], info['self_id']),  # 是否是 at 我
                } if info['message_type'] == "group" else None,

                "text": info['message'].extract_plain_text().strip(),  # 消息的 text 部分。（去除掉了表情、at 和多媒体数据）
                "images": extract_images(info['message']),  # 图片路径
            },
        }
    elif res['type'] == "notice":
        pass
        # return {
        #     **res,
        #     "notice": {  # 如果 update 类型是 notice 的话
        #         # TODO 暂时未实现
        #     }
        # }


def xhup_2_cq(info):
    """
    将 xhup 消息转换成 cqhttp 需要的格式
    :param info:
    :return:
    """
    reply_msg = info['message']
    msg_type = reply_msg['type']
    res = {
        "message_type": msg_type,
        "user_id": None,
        "group_id": None,
        "message": Message(),
    }

    if msg_type == "private":
        res['user_id'] = reply_msg['user']['id']
    elif msg_type == "group":
        res['group_id'] = reply_msg['group']['id']
        at_members = reply_msg['group']['at_members']
        if at_members:
            for m_id in at_members:
                res['message'].append(
                    MessageSegment.at(m_id))

    # 组建 Message
    if reply_msg['text']:
        res['message'].append(
            MessageSegment.text(reply_msg['text']))
    # if reply_msg['images']:  # 图片暂不支持
    #     for img in reply_msg['images']:
    #         info['message'].append(
    #             MessageSegment.image())

    return res
