from nonebot import require, on_command, on_keyword

from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message

from nonebot.params import CommandStart, EventMessage
from nonebot.log import logger

# test_action = on_command('test', aliases={'测试'})
test_action = on_keyword({'test'})

@test_action.handle()
async def _test_action(bot: Bot, event: GroupMessageEvent):
    await bot.call_api('send_group_sign', group_id=event.group_id)