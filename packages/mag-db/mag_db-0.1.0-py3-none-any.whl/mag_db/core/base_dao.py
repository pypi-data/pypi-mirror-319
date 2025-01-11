from typing import Any, Dict, List, Type

import pymysql
from mag_tools.exception.dao_exception import DaoException
from mag_tools.log.logger import Logger
from mag_tools.model.log_type import LogType

from mag_db.builder.select import Select
from mag_db.core.db_session import DBSession
from mag_db.manager.datasource_mgr import DatasourceMgr
from mag_db.sql.index_query_executor import IndexQueryExecutor


class BaseDao:
    _session = None

    def __init__(self):
        self._session = DBSession(DatasourceMgr.get_datasource('default'))

    def set_datasource(self, ds_name: str):
        self._session = DBSession(DatasourceMgr.get_datasource(ds_name))

    def insert_by_sql(self, insert_sql:str):
        try:
            with self._session.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(insert_sql)
                    conn.commit()
        except pymysql.MySQLError as e:
            raise DaoException(f"插入数据库出错：{str(e)}")

    def update_by_sql(self, update_sql:str):
        try:
            with self._session.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(update_sql)
                    conn.commit()
        except pymysql.MySQLError as e:
            raise DaoException(f"更新数据库出错：{str(e)}")

    def query_by_sql(self, query_sql:str)->list[Dict[str, Any]]:
        try:
            with self._session.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query_sql)
                    column_names = [description[0] for description in cursor.description]
                    results = [dict(zip(column_names, row)) for row in cursor.fetchall()]
                    return results
        except pymysql.MySQLError as e:
            raise DaoException(f"查询数据库出错：{str(e)}")

    def delete_by_sql(self, delete_sql:str):
        try:
            with self._session.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(delete_sql)
                    conn.commit()
        except pymysql.MySQLError as e:
            raise DaoException(f"删除数据库出错：{str(e)}")

    def total_count(self, table_name:str) -> int:
        select = Select([table_name], ['*'], None)
        query = IndexQueryExecutor(select.__str__(), self._session)
        return query.get_count()

    def test(self) -> bool:
        try:
            with self._session.connect() as conn:
                return conn is not None
        except (DaoException, pymysql.MySQLError) as e:
            Logger.error(LogType.DAO, e)
            return False

    @property
    def datasource_name(self):
        return self._session.datasource_name