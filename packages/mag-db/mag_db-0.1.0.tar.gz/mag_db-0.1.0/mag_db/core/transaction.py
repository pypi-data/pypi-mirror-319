from mag_tools.log.logger import Logger
from mag_tools.model.log_type import LogType

from mag_db.core.transaction_caches import TransactionCacheMgr


class Transaction:
    def __init__(self, name=None, datasource=None, parent=None):
        self.is_commit = False
        self.is_rollback = False
        self.is_end = False
        self.name = name
        self.datasource = datasource
        self.connection = None
        self.parent = parent

        if parent:
            self.data_source = parent.data_source

    @property
    def ds_name(self):
        return self.datasource.name if self.datasource else None

    def get_connection(self):
        return self.connection if self.parent is None else self.parent.get_connection()

    def set_connection(self, connection):
        if self.parent is None:
            self.connection = connection
        else:
            self.parent.set_connection(connection)

    def begin_with_connection(self):
        try:
            self.connection = self.data_source.get_connection()
            self.connection.autocommit(False)
            TransactionCacheMgr.get_tx_cache_by_name(self.ds_name).append(self)
        except Exception as e:
            self.close()
            Logger.throw(LogType.DAO, f"启动事务[{self.name}]失败: {str(e)}")

    def begin_without_connection(self):
        TransactionCacheMgr.get_tx_cache_by_name(self.ds_name).append(self)

    def commit(self):
        if self.is_commit or self.is_end:
            Logger.throw(LogType.DAO, f"提交事务[{self.name}]失败")

        try:
            self.do_commit()
        finally:
            self.is_commit = True

    def rollback(self):
        if self.is_rollback or self.is_end:
            Logger.throw(LogType.DAO, f"回滚事务[{self.name}]失败")

        try:
            self.do_rollback()
        finally:
            self.is_rollback = True

    def end(self):
        if self.is_end:
            Logger.throw(LogType.DAO, f"结束事务[{self.name}]失败")

        try:
            self.do_end()
            if not self.is_commit and not self.is_rollback:
                Logger.throw(LogType.DAO, f"结束事务[{self.name}]失败")
        finally:
            self.is_end = True

    def assert_open(self):
        if self.is_end or self.is_commit or self.is_rollback:
            Logger.throw(LogType.DAO,  f"断言事务[{self.name}]失败")

    def do_rollback(self):
        try:
            if self.parent is None:
                self.connection.rollback()
                self.connection.autocommit(True)
        except Exception as e:
            Logger.throw(LogType.DAO, f"回滚事务[{self.name}]失败：{str(e)}")

    def do_end(self):
        try:
            if self.parent is None:
                self.close()
        finally:
            TransactionCacheMgr.get_tx_cache_by_name(self.ds_name).remove(self)

    def close(self):
        try:
            if self.connection:
                self.connection.close()
        except Exception as e:
            Logger.throw(LogType.DAO, f"关闭事务[{self.name}]失败：{str(e)}")
        finally:
            self.connection = None

    def do_commit(self):
        try:
            if self.parent is None:
                self.connection.commit()
                self.connection.autocommit(True)
        except Exception as e:
            Logger.throw(LogType.DAO, f"提交事务[{self.name}]失败：{str(e)}")