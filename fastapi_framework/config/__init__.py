from .setting import get_setting, TortoiseORMSetting

setting = get_setting('config/config.toml')

ORM_LINK_CONF = TortoiseORMSetting(setting.db).orm_link_config