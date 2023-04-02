from nonebot import require, on_command

from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER

from nonebot.params import CommandArg
from nonebot.log import logger

require("nonebot_plugin_access_control")
from nonebot_plugin_access_control.service import create_plugin_service

ac = create_plugin_service('gm')
mute_ac = ac.create_subservice('mute')
kick_ac = ac.create_subservice('kick')

# need group perm and (person perm or group admin)
is_gm = GROUP_OWNER | GROUP_ADMIN

mute_action = on_command('mute', aliases={'禁言', 'unmute', '解禁'}, permission=is_gm)
mute_ac.patch_matcher(mute_action)
kick_action = on_command('kick', aliases={'踢人', '踢出', '踢'}, permission=is_gm)
kick_ac.patch_matcher(kick_action)


@mute_action.handle()
async def _mute_action(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):

    message = event.original_message

    if len(arg) < 1 or arg[0].type != 'at':
        return

    if 'mute' in message[0].data['text'] or '禁言' in message[0].data['text']:
        time = 5*60

        if len(arg) == 2:
            if arg[1].data['text'][-1].isdigit():
                time = int(arg[1].data['text'][1:])*60
            elif arg[1].data['text'][-1] == 'm':
                time = int(arg[1].data['text'][1:-1])*60
            elif arg[1].data['text'][-1] == 'h':
                time = int(arg[1].data['text'][1:-1])*60*60
            elif arg[1].data['text'][-1] == 'h':
                time = int(arg[1].data['text'][1:-1])*60*60*24

        await bot.set_group_ban(group_id=event.group_id, user_id=arg[0].data['qq'], duration=time)

    elif 'unmute' in message[0].data['text'] or '解禁' in message[0].data['text']:

        await bot.set_group_ban(group_id=event.group_id, user_id=arg[0].data['qq'], duration=0)


@kick_action.handle()
async def _kick_action(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):

    if len(arg) < 1 or arg[0].type != 'at':
        return

    await bot.set_group_kick(group_id=event.group_id, user_id=arg[0].data['qq'])
