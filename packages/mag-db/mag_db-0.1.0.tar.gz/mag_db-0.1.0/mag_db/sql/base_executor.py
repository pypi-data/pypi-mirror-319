from typing import List, Optional

import pymysql
from pymysql import Connection
from pymysql.cursors import Cursor
from mag_tools.exception.dao_exception import DaoException
from mag_tools.log.logger import Logger
from mag_tools.model.log_type import LogType

from mag_db.core.db_session import DBSession
from mag_db.bean.table import Table
from mag_db.core.transaction import Transaction
from mag_db.utils.sql_parser import SqlParser


class BaseExecutor:
    def __init__(self, sql: str, session: DBSession):
        if not sql:
            raise ValueError('sql cannot be empty')

        self._tables = SqlParser.get_tables(sql)

        # “表别名.列名”转换为“表名.列名”
        self._sql = SqlParser.convert_column_name(sql, self._tables)
        self._column_names = SqlParser.get_column_names(self._sql)
        self._session = session

    def set_tables(self, tables: List[Table]):
        self._tables = tables
        self._sql = SqlParser.convert_column_name(self._sql, self._tables)

    def get_connection(self, tx: Optional[Transaction] = None)->Connection:
        con = None

        try:
            # 取得当前未结束的事务
            if tx:
                tx.assert_open()
                # 如果SQL操作属于某个事务，则从该事务中取得连接
                con = tx.get_connection()
            else:
                # 无事务则直接取得新的连接
                if self._session is None:
                    raise DaoException("找不到有用数据库会话")

                con = self._session.connect()

            if con is None:
                raise DaoException("数据库连接不能为空")
        except DaoException as e:
            Logger.throw(LogType.DAO, f"取数据库连接失败: {str(e)}")

        return con

    @classmethod
    def close_connection(cls, con: Connection, tx: Transaction = None, cursor: Cursor = None):
        try:
            if cursor:
                cursor.close()
        except pymysql.MySQLError:
            pass

        try:
            # 无事务则直接关闭连接, 否则数据库连接随相应事务关闭而关闭
            if tx is None and con:
                con.close()
        except pymysql.MySQLError:
            pass

        try:
            if tx:
                tx.close()
        except pymysql.MySQLError:
            pass

    def prepare(self):
        raise NotImplementedError("init() must be implemented by subclasses")