from nonebot import require, on_message

from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent

from nonebot.rule import Rule
from nonebot.log import logger
from nonebot.typing import T_State

require("nonebot_plugin_access_control")
from nonebot_plugin_access_control.service import create_plugin_service

import re
import asyncio
from ...config import get_config

ac = create_plugin_service('reply')
config = get_config()


async def reply_match(event: GroupMessageEvent, state: T_State) -> bool:
    if event.group_id not in config['reply']['groups']:
        return False
    
    for i in config['reply']['groups'][event.group_id]['dicts'].keys():
        if re.search(r'' + i, event.message.extract_plain_text()) != None:
            state['reply_msg']  = config['reply']['groups'][event.group_id]['dicts'][i]
            return True

    return False


reply_check = Rule(reply_match)
reply_action = on_message(rule=reply_check)
ac.patch_matcher(reply_action)

@reply_action.handle()
async def _reply_action(bot: Bot, event: GroupMessageEvent, state: T_State):
    fmt = {'qq': event.user_id, 'group_qq': event.group_id}
    await bot.send_group_msg(group_id=event.group_id, message=state['reply_msg'].format(**fmt))

