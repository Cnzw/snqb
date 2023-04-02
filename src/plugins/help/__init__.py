from nonebot import require, on_command

from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment

from nonebot.log import logger

require("nonebot_plugin_access_control")
from nonebot_plugin_access_control.service import create_plugin_service

from pathlib import Path

ac = create_plugin_service('help')

help_action = on_command('menu', aliases={'机器人菜单', '机器人帮助'})
ac.patch_matcher(help_action)

@help_action.handle()
async def _help_action(bot: Bot, event: GroupMessageEvent):
    pth = Path('./src/res/help.jpg')
    await help_action.finish(MessageSegment.image(pth))