from nonebot import require, on_command

from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment

from nonebot.log import logger

require("nonebot_plugin_access_control")
from nonebot_plugin_access_control.service import create_plugin_service

import random
import httpx
from pathlib import Path
import re
from ...config import get_config


config = get_config()
ac = create_plugin_service('setu')

setu_action = on_command('色图', aliases={'涩涩', '涩图', '色色'})
ac.patch_matcher(setu_action)

@setu_action.handle()
async def _setu_action(bot: Bot, event: GroupMessageEvent):
    # 10 3-yellow 3-no sese! 4-pic
    rnd = random.randint(0,100)
    if rnd <= 20:
        pth = Path('./src/res/setu.jpg')
        msg = [
            {
                "type": "node",
                "data": {
                    "name": "Jitsu API",
                    "uin": event.self_id,
                    "content": MessageSegment.image(pth)
                }
            },
                        {
                "type": "node",
                "data": {
                    "name": "Jitsu API",
                    "uin": event.self_id,
                    "content": "pth: 3397f1b55f54523160752297d269ee0e"
                }
            },
            {
                "type": "node",
                "data": {
                    "name": "Jitsu API",
                    "uin": event.self_id,
                    "content": "(+60s CD)"
                }
            }
        ]
        await bot.send_group_forward_msg(group_id=event.group_id, messages=msg)

    elif rnd <= 40:
        payloads: list[str] = config['setu-msg']
        msg = random.choice(payloads) + '(+60s CD)'
        await setu_action.finish(msg)
    
    else:
        if rnd <= 45:
            url = 'https://moe.jitsu.top/img/?sort=setu&type=json'
        url = 'https://moe.jitsu.top/img/?sort=mp&type=json'
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            result = resp.json()
        
        logger.debug(result)
        imgUrl: str = result['pics'][0] + '?x-bce-process=image/resize,limit_1,p_20'
        pth = re.match(r'https://pic\.rmb.bdstatic\.com/bjh/([a-z0-9]+)', result['pics'][0]).group(1)
        

        # msg = Message(MessageSegment.image(imgUrl) + f'\npth: {pth}\n(+60s CD) 图片By JitsuAPI')
        msg = [
            {
                "type": "node",
                "data": {
                    "name": "Jitsu API",
                    "uin": event.self_id,
                    "content": MessageSegment.image(imgUrl)
                }
            },
                        {
                "type": "node",
                "data": {
                    "name": "Jitsu API",
                    "uin": event.self_id,
                    "content": f"pth: {pth}"
                }
            },
            {
                "type": "node",
                "data": {
                    "name": "Jitsu API",
                    "uin": event.self_id,
                    "content": "(+60s CD)"
                }
            }
        ]

        await bot.send_group_forward_msg(group_id=event.group_id, messages=msg)