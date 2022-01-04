from configobj import ConfigObj

conf = ConfigObj("./config/config.ini")
global_config = conf["global"]


def get_config(key: str):
    global global_config
    return global_config[key]


def check_test_mode():
    return get_config("test_mode")
