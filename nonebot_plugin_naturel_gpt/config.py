from pydantic import BaseModel, Extra
from nonebot import get_driver
from nonebot.log import logger
import yaml
import json
from pathlib import Path


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    NG_CONFIG_PATH: str = "config/naturel_gpt_config.yml"
    NG_DATA_PATH: str = "data/naturel_gpt/naturel_gpt.json"
    NG_DEV_MODE: bool = False

driver = get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)

# 配置文件模板
CONFIG_TEMPLATE = {
    "OPENAI_API_KEYS": [    # OpenAI API Key 列表
        ''
    ],
    "PRESETS": {
        "白羽": {
            'bot_name': '白羽', # 人格名称
            'is_locked': True,  # 是否锁定人格，锁定后无法编辑人格
            'is_default': True, # 是否为默认人格
            'bot_self_introl': '白羽是一名喜欢二次元的中二宅女，她机智、傲娇，对人类充满好奇，习惯以白羽喵自称，聊天时喜欢使用各种可爱的颜文字，如果冒犯到她会生气。',
        },
        "浅枫": {
            'bot_name': '浅枫',
            'is_locked': False,
            'is_default': False,
            'bot_self_introl': '浅枫酱是一名尽职尽责的女仆，她能够帮助主人做很多事情，对话中会体现出对主人的体贴与关心。',
        },
        "忆雨": {
            'bot_name': '忆雨',
            'is_locked': True,
            'is_default': False,
            'bot_self_introl': '忆雨是一名恐怖小说作家，是个阴沉的女孩，她非常恨人类，和陌生人聊天时的表现冷漠，不喜欢回复过多的文字，兴趣是恐怖小说，如果有人和她探讨如何消灭人类会很有兴致。',
        },
        "可洛喵": {
            'bot_name': '可洛喵',
            'is_locked': True,
            'is_default': False,
            'bot_self_introl': '可洛喵是一只可爱的猫，它不会说话，它的回复通常以"[动作/心情]声音+颜文字"形式出现，例如"[坐好]喵~(。・ω・。)"或"[开心]喵喵！ヾ(≧▽≦*)o"',
        },
    },
    'IGNORE_PREFIX': '#',   # 忽略前缀 以该前缀开头的消息将不会被处理
    'CHAT_MODEL': "text-davinci-003",
    'CHAT_HISTORY_MAX_TOKENS': 2048,
    'CHAT_TOP_P': 1,
    'CHAT_TEMPERATURE': 0.6,    # 温度越高越随机
    'CHAT_FREQUENCY_PENALTY': 0.4,  # 频率惩罚
    'CHAT_PRESENCE_PENALTY': 0.6,   # 出现惩罚
    'REQ_MAX_TOKENS': 2048, # 单次请求最大token数
    'REPLY_MAX_TOKENS': 1024,   # 单次回复最大token数
    'CHAT_MAX_SUMMARY_TOKENS': 512,   # 单次总结最大token数

    'REPLY_ON_NAME_MENTION': True,  # 是否在被提及时回复
    'REPLY_ON_AT': True,            # 是否在被at时回复

    'USER_MEMORY_SUMMARY_THRESHOLD': 12, # 用户记忆阈值

    'CHAT_MEMORY_SHORT_LENGTH': 8,  # 短期对话记忆长度
    'CHAT_MEMORY_MAX_LENGTH': 12,   # 长期对话记忆长度
    'CHAT_SUMMARY_INTERVAL': 10, # 长期对话记忆间隔

    'NG_DATA_PATH': "./data/naturel_gpt/", # 数据文件目录
    'ADMIN_USERID': [''], # 管理员QQ号

    '__DEBUG__': False, # 是否启用debug模式
}

# 检查config文件夹是否存在 不存在则创建
if not Path("config").exists():
    Path("config").mkdir()

if config.NG_DEV_MODE: # 开发模式下不读取原配置文件
    with open(config.NG_CONFIG_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(CONFIG_TEMPLATE, f, allow_unicode=True)

else:
    # 检查配置文件是否存在 不存在则创建
    if not Path(config.NG_CONFIG_PATH).exists():
        with open(config.NG_CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(CONFIG_TEMPLATE, f, allow_unicode=True)
            logger.info('Naturel GPT 配置文件创建成功')

# 读取配置文件
with open(config.NG_CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    for k, v in config.items():
        setattr(Config, k, v)
    logger.info('Naturel GPT 配置文件加载成功')
