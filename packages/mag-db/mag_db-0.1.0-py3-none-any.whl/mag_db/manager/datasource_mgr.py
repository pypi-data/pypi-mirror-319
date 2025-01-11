from mag_tools.config.sys_config import SysConfig

from mag_db.handler.type_handler_factory import TypeHandlerFactory
from mag_db.bean.datasource_info import DatasourceInfo


class DatasourceMgr:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(DatasourceMgr, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):  # 避免重复初始化
            self.datasources = {}
            for key, value in SysConfig.get_datasources().items():
                ds = DatasourceInfo.load_map(value)
                ds.name = key.lower()
                self.datasources[ds.name] = ds

            if len(self.datasources) > 0:
                TypeHandlerFactory.initialize()

            self._initialized = True

    @classmethod
    def get_datasource(cls, datasource_name):
        return cls().datasources[datasource_name.lower()]
