import openai
from loguru import logger
from json import loads
from random import choice
from gameyamlspiderandgenerator.hook import BaseHook
from gameyamlspiderandgenerator.util.config import config


class OpenAI(BaseHook):
    CHANGED = None
    REQUIRE_CONFIG = True

    def setup(self, data: dict):
        chat_dict = [{"role": "user", "content": data["description"] + "\nvisual-novel strategy real-time-strategy "
                                                                       "casual business-sim adventure board action "
                                                                       "fantasy fighting music shooter puzzle "
                                                                       "role-playing mmorpg dating-sim roguelike "
                                                                       "sports non-indie bara yuri yiff gore comedy "
                                                                       "tragedy horror "
                                                                       "根据以上游戏介绍**只用**以上所给出的英文标签给这个游戏打上最有可能的标签，输出为json，不需要带键名\n如果实在没有相匹配的标签输出空列表[]"}]
        openai.api_key = config["hook_config"]["openai"]['api_key']
        openai.proxy = config["proxy"]
        rzt = openai.ChatCompletion.create(model=config["hook_config"]["openai"]['model'], messages=chat_dict)
        logger.info("tags that may exist: " + ', '.join(loads(choice(rzt["choices"])["message"]["content"])))
        return data
