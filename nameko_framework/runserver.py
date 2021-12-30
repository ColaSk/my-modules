from conf.setting import Setting
from main import main

"""Service startup
"""
class args:
    config = Setting.CONFIG_YAML
    services = Setting.INSTALLED_SERVICES
    backdoor_port = None

if __name__=="__main__":
    main(args)