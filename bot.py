import nonebot
# from nonebot.adapters.mirai2 import Adapter as MIRAI2Adapter

# from nonebot.adapters.console import Adapter as CONSOLEAdapter

from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter



nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
# driver.register_adapter(MIRAI2Adapter)

# driver.register_adapter(CONSOLEAdapter)

driver.register_adapter(ONEBOT_V11Adapter)

nonebot.load_builtin_plugins('echo', 'single_session')
# nonebot.load_plugins("src/plugins")


nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run()