from nonebot import require, on_notice

from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import PokeNotifyEvent

from nonebot.rule import Rule, to_me
# from nonebot.log import logger

require("nonebot_plugin_access_control")
from nonebot_plugin_access_control.service import create_plugin_service

import asyncio
import random
from ...config import get_config


ac = create_plugin_service('poke')
config = get_config()

# async def is_poke(event: PokeNotifyEvent) -> bool:
#     return (event.sub_type == "poke" and event.is_tome())

# poke_check = Rule(is_poke)

poke_action = on_notice(rule=to_me())
ac.patch_matcher(poke_action)


@poke_action.handle()
async def _poke_action(bot: Bot, event: PokeNotifyEvent):
    if event.group_id == None: return
    msg: str = random.choice(config['poke']['groups'][event.group_id]['playloads'])
    fmt = {'qq': event.user_id, 'group_qq': event.group_id}
    await bot.send_group_msg(group_id=event.group_id, message=msg.format(**fmt))