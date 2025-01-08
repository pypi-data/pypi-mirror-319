import os
import json
from typing import Any, Dict


class SysConfig:
    __instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(SysConfig, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        # 获取工程的根目录
        self.root_dir = os.getcwd()

        # 读取配置文件
        self.config = self.__load_config()

    @classmethod
    def root_dir(cls):
        return cls().root_dir

    @classmethod
    def resource_dir(cls):
        return os.path.join(cls().root_dir, 'resources')

    @classmethod
    def logging_conf(cls):
        return os.path.join(cls().root_dir, 'resources', 'config', 'logging.conf')

    @classmethod
    def get(cls, key: str, default=None):
        return cls().config.get(key, default)

    @classmethod
    def get_datasource_info(cls) -> Dict[str, Any]:
        return cls().config.get("datasource")

    def __load_config(self):
        config_file = os.path.join(self.root_dir, 'resources', 'config', 'sys_config.json')

        if not os.path.exists(config_file):
            raise FileNotFoundError(f"配置文件 {config_file} 不存在")

        with open(config_file, 'r', encoding='utf-8') as file:
            config = json.load(file)
        return config
