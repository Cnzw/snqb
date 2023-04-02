from nonebot import require, get_bot

from nonebot.adapters.onebot.v11.message import Message, MessageSegment

from nonebot.log import logger

require('nonebot_plugin_apscheduler')
from nonebot_plugin_apscheduler import scheduler

require("nonebot_plugin_access_control")
from nonebot_plugin_access_control.service import create_plugin_service

require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import md_to_pic

import re
import httpx
import random
import base64
from datetime import date
# from ...utils import download_url
from ...config import get_config

ac = create_plugin_service('scheduler')
config = get_config()


async def scheduler_group_action(qq: int, type: int, payloads: list):
    if not await ac.check_by_subject(f'qq:g{qq}'):
        return

    bot = get_bot('3198807326')

    if type == 0:

        msg0: str = random.choice(payloads)
        logger.success(f'定时任务 > 已向 {qq} 发送消息')
        await bot.send_group_msg(group_id=qq, message=msg0)

    elif type == 1:

        url = 'https://api.2xb.cn/zaob'
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            result = resp.json()

        if result['code'] == 200:
            # f'[CQ:image,file={result["imageUrl"]}]'
            msg1 = Message(MessageSegment.image(result["imageUrl"]))
        else:
            msg1 = Message([MessageSegment.text(
                f'早报获取失败: {result["code"]}'), MessageSegment.at(user_id=2939293760)])

        logger.success(f'定时任务 > 已向 {qq} 发送早报')
        await bot.send_group_msg(group_id=qq, message=msg1)

    elif type == 2:

        month = date.today().strftime("%m")
        day = date.today().strftime("%d")

        url1 = f"https://baike.baidu.com/cms/home/eventsOnHistory/{month}.json"
        async with httpx.AsyncClient() as client:
            resp1 = await client.get(url1)
            result1 = resp1.json()

        url2 = "https://zj.v.api.aa1.cn/api/nl/"
        async with httpx.AsyncClient() as client:
            resp2 = await client.get(url2)
            result2 = resp2.json()

        content = '<img width="100%" src="https://bing.icodeq.com"/>\n'
        content += f'<h1 align="center">历史上的今天</h1>\n'
        content += f'<p align="center">{result2["nl"]} {result2["today"][5:]} {result2["xq"]}</p>\n'
        for i in result1[month][month + day]:
            title = re.sub(r'<.*?>', '', i['title'])
            content += f' - {i["year"]}年 {title}\n'
        content += f'<hr><p align="right" style="color:gray"><small>数据By 百度百科 | 生成By 星网互联</small></p>'

        img = await md_to_pic(md=content)
        # f'[CQ:image,file=base64://{base64.b64encode(img).decode()}]'
        msg2 = Message(MessageSegment.image(img))

        logger.success(f'定时任务 > 已向 {qq} 发送历史上的今天')
        await bot.send_group_msg(group_id=qq, message=msg2)

    elif type == 3:

        logger.success(f'定时任务 > 已向 {qq} 发送群打卡')
        await bot.send_group_sign(group_id=qq)


schedulers = list(config['scheduler']['groups'].keys())
for i in range(len(schedulers)):
    for task in config['scheduler']['groups'][schedulers[i]]['tasks']:
        scheduler.add_job(scheduler_group_action, 'cron', day_of_week=task['day_of_week'], hour=task['hour'], minute=task['minute'], args=[
            schedulers[i], task['type'], task['payloads']])
