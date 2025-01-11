
from mag_tools.log.logger import Logger
from mag_tools.model.log_type import LogType

from mag_db.core.transaction_caches import TransactionCacheMgr
from mag_db.sql.base_executor import BaseExecutor


class UpdateExecutor(BaseExecutor):
    def execute(self):
        self.check()

        try:
            values = self.prepare()

            tx = TransactionCacheMgr.get_current_tx(self._session.datasource_name.name)
            connection = self.get_connection(tx)
            with connection.cursor() as cursor:
                cursor.execute(self._sql, values)

        except Exception as e:
            Logger.throw(LogType.DAO,f"执行SQL失败: {self._sql}")

    def check(self):
        raise NotImplementedError("Subclasses should implement this method")

    def prepare(self):
        raise NotImplementedError("Subclasses should implement this method")
