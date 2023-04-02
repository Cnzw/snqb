from nonebot import require, on_command

from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message ,MessageSegment

from nonebot.params import CommandArg, Arg
from nonebot.typing import T_State
from nonebot.log import logger

require("nonebot_plugin_access_control")
from nonebot_plugin_access_control.service import create_plugin_service

require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import md_to_pic

import httpx
from typing import Any, Dict, List


ac = create_plugin_service('music')

music_action = on_command('music', aliases={'点歌', '音乐', '听歌', '搜歌', '播放'})
ac.patch_matcher(music_action)


@music_action.handle()
async def _music_action(bot: Bot, event: GroupMessageEvent, state: T_State, arg: Message = CommandArg()):

    # message = event.original_message
    
    if len(arg) != 1 or arg[0].type != 'text': # no args or has other msg type
        await music_action.finish('请输入歌曲名，如 `点歌 好运来`')
    
    args: list[str] = arg[0].data['text'].split(' ')

    if len(args) > 1 and args[-1].isdigit():
        has_id = True
        kw: str = ' '.join(args[:-1])
    else:  # no id
        has_id = False
        kw: str = ' '.join(args)

    try:
        songs_list = await search_163(kw)

    except Exception as e:
        logger.warning(e)
        await music_action.finish('未搜索到对应结果: 内部错误')

    else:
        if len(songs_list) == 0:
            await music_action.finish('未搜索到对应结果')

        if has_id:
            if not 1 <= int(args[-1]) <= len(songs_list):
                await music_action.finish(f'数字范围: 1-{len(songs_list)}')

            await music_action.finish(MessageSegment.music('163', songs_list[int(args[-1]) - 1]["id"]))

        state['song_list'] = songs_list

        content = f'<h3 align="center">网易云 {kw} 搜索结果</h3>\n|id|歌名|作者|\n|---|---|---|\n'
        for i in range(len(songs_list)):
            content += f'|{i+1}|{songs_list[i]["name"]}|{songs_list[i]["artist"]}|\n'
        content += f'\n**你可以直接输入 `数字` (歌曲id)来选择歌曲**\n'
        content += '<p align="right" style="color:gray"><small>数据By 网易云 | 生成By 星网互联</small></p>'

        img = await md_to_pic(md=content)
        await music_action.send(MessageSegment.image(img))


@music_action.got('id')
async def _music_action_got(bot: Bot, event: GroupMessageEvent, state: T_State, id: Message = Arg()):
    logger.debug(id)

    if len(id) != 1 or id[0].type != 'text': # once is over
        await music_action.finish()

    msg = id[0].data['text']

    if msg.isdigit():
        if not 1 <= int(msg) <= len(state['song_list']):
            await music_action.finish('数字超出范围，请重新点歌。如 `点歌 好运来 1`') # 
        
        await music_action.finish(MessageSegment.music('163',state['song_list'][int(msg) - 1]["id"]))
        


async def search_163(keyword: str):
    url = "https://music.163.com/api/cloudsearch/pc"
    params = {"s": keyword, "type": 1, "offset": 0}
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, params=params)
        result = resp.json()
    songs: List[Dict[str, Any]] = result["result"]["songs"]
    
    output: List[Dict[str, Any]] = []
    if songs:
        for i in range(len(songs)):
            output.append(
                {'name': songs[i]['name'], 'artist': songs[i]['ar'][0]['name'], 'id': songs[i]['id']})

    return output

# async def search_qq(keyword: str):
#     url = "https://c.y.qq.com/splcloud/fcgi-bin/smartbox_new.fcg"
#     params = {
#         "format": "json",
#         "inCharset": "utf-8",
#         "outCharset": "utf-8",
#         "notice": 0,
#         "platform": "yqq.json",
#         "needNewCode": 0,
#         "uin": 0,
#         "hostUin": 0,
#         "is_xml": 0,
#         "key": keyword,
#     }
#     async with httpx.AsyncClient() as client:
#         resp = await client.get(url, params=params)
#         result = resp.json()
#     songs: List[Dict[str, str]] = result["data"]["song"]["itemlist"]
#     if songs:
#         songs.sort(
#             key=lambda x: SequenceMatcher(None, keyword, x["name"]).ratio(),
#             reverse=True,
#         )
#         return f'[CQ:music,type=qq,id={int(songs[0]["id"])}]'
