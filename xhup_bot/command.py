# -*- coding: utf-8 -*-
import logging
import re
from collections import OrderedDict

from aiocqhttp import CQHttp
from aiocqhttp.message import Message, MessageSegment
from typing import Callable, Pattern, Dict, Any, Iterable

from config import BotConfig

"""
QQ消息解析模块
"""

logger = logging.getLogger(__name__)

# 群聊命令
_group_registry: OrderedDict = OrderedDict()

# 私聊命令
_private_registry: OrderedDict = OrderedDict()


def on_group_command(
        pattern: Pattern,
        at_me: bool = True,
        usage: str = None,
) -> Callable:
    """
    注册群聊命令
    :return:
    """

    def deco(func: Callable) -> Callable:
        nonlocal pattern

        if isinstance(pattern, str):
            pattern = re.compile(pattern)

        _group_registry[pattern] = {
            "handler": func,
            "at_me": at_me,
            "usage": usage if usage else "无"
        }

        return func

    return deco


def on_private_command(
        pattern: Pattern,
        usage: str = None,
) -> Callable:
    """
    注册私聊命令
    :return:
    """

    def deco(func: Callable) -> Callable:
        nonlocal pattern

        if isinstance(pattern, str):
            pattern = re.compile(pattern)

        _private_registry[pattern] = {
            "handler": func,
            "usage": usage if usage else "无"
        }

        return func

    return deco


async def handle_group_message(bot: CQHttp, context: Dict[str, Any]):
    """
    处理群聊消息，只处理文字
    :param bot:
    :param context:
    :return:
    """
    _log_message(context)

    if not context['message']:
        context['message'].append(MessageSegment.text(''))

    # 处理 at_me
    raw_to_me = context.get('to_me', False)
    _check_at_me(bot, context)
    _check_calling_me_nickname(bot, context)
    context['to_me'] = raw_to_me or context['to_me']

    group_id = context['group_id']
    user_role = context['sender']['role']
    for pattern, data in _group_registry.items():
        matcher = pattern.fullmatch(context['message'].extract_plain_text())
        if matcher:
            if data['at_me'] and not context['to_me']:  # 该命令需要 at_me，但是却没有
                return

            # TODO 处理命令权限问题（鹤主群只允许管理员查询）

            await data['handler'](bot, context, matcher.groupdict())


async def handle_private_message(bot: CQHttp, context: Dict[str, Any]):
    """
    处理私聊消息
    :param bot:
    :param context:
    :return:
    """
    _log_message(context)

    for pattern, data in _private_registry.items():

        matcher = pattern.fullmatch(context['message'].extract_plain_text())
        if matcher:
            await data['handler'](bot, context, matcher.groupdict())


def _check_at_me(bot: CQHttp, context: Dict[str, Any]) -> None:
    if context['message_type'] == 'private':
        context['to_me'] = True
    else:
        # group or discuss
        context['to_me'] = False
        at_me_seg = MessageSegment.at(context['self_id'])

        # check the first segment
        first_msg_seg = context['message'][0]
        if first_msg_seg == at_me_seg:
            context['to_me'] = True
            del context['message'][0]

        if not context['to_me']:
            # check the last segment
            i = -1
            last_msg_seg = context['message'][i]
            if last_msg_seg.type == 'text' and \
                    not last_msg_seg.data['text'].strip() and \
                    len(context['message']) >= 2:
                i -= 1
                last_msg_seg = context['message'][i]

            if last_msg_seg == at_me_seg:
                context['to_me'] = True
                del context['message'][i:]

        if not context['message']:
            context['message'].append(MessageSegment.text(''))


def _check_calling_me_nickname(bot: CQHttp, context: Dict[str, Any]) -> None:
    first_msg_seg = context['message'][0]
    if first_msg_seg.type != 'text':
        return

    first_text = first_msg_seg.data['text']

    if BotConfig.NICKNAME:
        # check if the user is calling me with my nickname
        if isinstance(BotConfig.NICKNAME, str) or \
                not isinstance(BotConfig.NICKNAME, Iterable):
            nicknames = (BotConfig.NICKNAME,)
        else:
            nicknames = filter(lambda n: n, BotConfig.NICKNAME)
        nickname_regex = '|'.join(nicknames)
        m = re.search(rf'^({nickname_regex})([\s,，]*|$)',
                      first_text, re.IGNORECASE)
        if m:
            nickname = m.group(1)
            logger.debug(f'User is calling me {nickname}')
            context['to_me'] = True
            first_msg_seg.data['text'] = first_text[m.end():]


def _log_message(context: Dict[str, Any]) -> None:
    msg_from = str(context['user_id'])
    if context['message_type'] == 'group':
        msg_from += f'@[群:{context["group_id"]}]'
    elif context['message_type'] == 'discuss':
        msg_from += f'@[讨论组:{context["discuss_id"]}]'
    logger.info(f'Self: {context["self_id"]}, '
                f'Message {context["message_id"]} from {msg_from}: '
                f'{context["message"]}')
