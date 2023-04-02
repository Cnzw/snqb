from nonebot import require, on_notice

from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent

from nonebot.log import logger

require("nonebot_plugin_access_control")
from nonebot_plugin_access_control.service import create_plugin_service

import random
from ...config import get_config


ac = create_plugin_service('member_change')
config = get_config()


# async def is_members_increase_change(event: GroupIncreaseNoticeEvent) -> bool:
#     return event.notice_type == 'group_increase'

# async def is_members_decrease_change(event: GroupDecreaseNoticeEvent) -> bool:
#     return event.notice_type == 'group_decrease'

# members_change_increase_check = Rule(is_members_increase_change)
# members_change_decrease_check = Rule(is_members_decrease_change)

members_change_increase_action = on_notice()
members_change_decrease_action = on_notice()

increase_ac = ac.create_subservice('increase')
increase_ac.patch_matcher(members_change_increase_action)
decrease_ac = ac.create_subservice('decrease')
decrease_ac.patch_matcher(members_change_decrease_action)


@members_change_increase_action.handle()
async def _members_change_increase_action(bot: Bot, event: GroupIncreaseNoticeEvent):
    msg: str = random.choice(config['members-change']
                        [event.group_id]['increase']['payloads'])
    fmt = {'qq': event.user_id, 'group_qq': event.group_id}
    await bot.send_group_msg(group_id=event.group_id, message=msg.format(**fmt))


@members_change_decrease_action.handle()
async def _members_change_decrease_action(bot: Bot, event: GroupDecreaseNoticeEvent):
    msg: str = random.choice(config['members-change']
                        [event.group_id]['decrease']['payloads'])
    fmt = {'qq': event.user_id, 'group_qq': event.group_id}
    await bot.send_group_msg(group_id=event.group_id, message=msg.format(**fmt))
