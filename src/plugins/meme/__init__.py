from nonebot import require, on_regex, on_command, CommandGroup

from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message ,MessageSegment

from nonebot.params import RegexGroup, CommandArg
from nonebot.typing import T_Handler, T_State
from nonebot.log import logger

require("nonebot_plugin_access_control")
from nonebot_plugin_access_control.service import create_plugin_service

from typing import Any, Tuple
import base64
from meme_generator import get_meme
# from ...config import get_config
from ...utils import download_url

ac = create_plugin_service('meme')


def only_str_args_action() -> T_Handler:
    async def _one_str_arg_action(bot: Bot, event: GroupMessageEvent, state: T_State, arg: Message = CommandArg()):

        if len(arg) != 1 or arg[0].type != 'text':
            return

        perm = await ac.get_child(state['meme_kw']).check_by_subject(f'qq:g{event.group_id}')
        if not perm:
            return

        meme = get_meme(state['meme_kw'])

        if meme.params_type.max_texts > 1:
            args: list[str] = arg[0].data['text'].split(' ')
            if len(args) != meme.params_type.max_texts:
                return
            img = await meme(images=[], texts=args)
        else:
            img = await meme(images=[], texts=[arg[0].data['text']])

        msg = f'[CQ:image,subType=1,file=base64://{base64.b64encode(img.getvalue()).decode()}]'
        # msg = Message(MessageSegment.image(img, ))
        await bot.send_group_msg(group_id=event.group_id, message=msg)

    return _one_str_arg_action


def one_pic_args_action() -> T_Handler:
    async def _one_pic_args_action(bot: Bot, event: GroupMessageEvent, state: T_State, arg: Message = CommandArg()):

        if len(arg) != 1 or arg[0].type not in ['text', 'at', 'image']:
            return
        
        perm = await ac.get_child(state['meme_kw']).check_by_subject(f'qq:g{event.group_id}')
        if not perm:
            return

        # message = event.original_message
        meme = get_meme(state['meme_kw'])

        # for seg in event.original_message:
        #     logger.debug(seg.type+str(seg.data))

        if arg[0].type == 'text' and arg[0].data['text'] in ['自己', '我', 'me', '俺']:
            img1 = await download_url(f'http://q1.qlogo.cn/g?b=qq&nk={event.user_id}&s=640')
            img = await meme(images=[img1], texts=[])

        elif arg[0].type == 'at':
            id = arg[0].data['qq']
            img2 = await download_url(f'http://q1.qlogo.cn/g?b=qq&nk={id}&s=640')
            img = await meme(images=[img2], texts=[])

        elif arg[0].type == 'image':
            url = arg[0].data['url']
            img3 = await download_url(url)
            img = await meme(images=[img3], texts=[])

        else:
            return

        msg = f'[CQ:image,subType=1,file=base64://{base64.b64encode(img.getvalue()).decode()}]'
        await bot.send_group_msg(group_id=event.group_id, message=msg)

    return _one_pic_args_action


cmdg = CommandGroup('表情')

ac.create_subservice('good_news')
# on_regex(r'^\.?表情 喜报 (.+)',
#          state={'meme_kw': 'good_news'}).append_handler(only_str_args_action())
cmdg.command('喜报', state={'meme_kw': 'good_news'}
             ).append_handler(only_str_args_action())

ac.create_subservice('bad_news')
cmdg.command('悲报',
             state={'meme_kw': 'bad_news'}).append_handler(only_str_args_action())

ac.create_subservice('douyin')
cmdg.command('抖音', state={'meme_kw': 'douyin'}
             ).append_handler(only_str_args_action())

ac.create_subservice('fanatic')
cmdg.command('真爱粉',
             state={'meme_kw': 'fanatic'}).append_handler(only_str_args_action())

ac.create_subservice('hold_grudge')
cmdg.command('记仇',
             state={'meme_kw': 'hold_grudge'}).append_handler(only_str_args_action())

ac.create_subservice('imprison')
cmdg.command('坐牢',
             state={'meme_kw': 'imprison'}).append_handler(only_str_args_action())

ac.create_subservice('murmur')
cmdg.command('低语', state={'meme_kw': 'murmur'}
             ).append_handler(only_str_args_action())

ac.create_subservice('shutup')
cmdg.command('别说了',
             state={'meme_kw': 'shutup'}).append_handler(only_str_args_action())

ac.create_subservice('pornhub')  # 2
cmdg.command('p站',
             state={'meme_kw': 'pornhub'}).append_handler(only_str_args_action())

ac.create_subservice('wangjingze')  # 4
cmdg.command('真香',
             state={'meme_kw': 'wangjingze'}).append_handler(only_str_args_action())

ac.create_subservice('youtube')  # 2
cmdg.command('油管',
             state={'meme_kw': 'youtube'}).append_handler(only_str_args_action())


ac.create_subservice('pat')
cmdg.command('拍',
         state={'meme_kw': 'pat'}).append_handler(one_pic_args_action())

ac.create_subservice('alike')
cmdg.command('一样',
         state={'meme_kw': 'alike'}).append_handler(one_pic_args_action())

ac.create_subservice('always')
cmdg.command('一直',
         state={'meme_kw': 'always'}).append_handler(one_pic_args_action())

ac.create_subservice('capoo_rub')
cmdg.command('蹭',
         state={'meme_kw': 'capoo_rub'}).append_handler(one_pic_args_action())

ac.create_subservice('confuse')
cmdg.command('妈妈生的',
         state={'meme_kw': 'confuse'}).append_handler(one_pic_args_action())

ac.create_subservice('hold_tight')
cmdg.command('抱紧',
         state={'meme_kw': 'hold_tight'}).append_handler(one_pic_args_action())

ac.create_subservice('listen_music')
cmdg.command('唱片',
         state={'meme_kw': 'listen_music'}).append_handler(one_pic_args_action())

ac.create_subservice('loading')
cmdg.command('加载中',
         state={'meme_kw': 'loading'}).append_handler(one_pic_args_action())

ac.create_subservice('rip_angrily')
cmdg.command('撕',
         state={'meme_kw': 'rip_angrily'}).append_handler(one_pic_args_action())

ac.create_subservice('trance')
cmdg.command('颠',
         state={'meme_kw': 'trance'}).append_handler(one_pic_args_action())

ac.create_subservice('turn')
cmdg.command('旋转',
         state={'meme_kw': 'turn'}).append_handler(one_pic_args_action())

ac.create_subservice('worship')
cmdg.command('膜拜',
         state={'meme_kw': 'worship'}).append_handler(one_pic_args_action())
