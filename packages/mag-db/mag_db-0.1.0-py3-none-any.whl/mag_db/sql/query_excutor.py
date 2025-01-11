import pymysql
from mag_tools.log.logger import Logger
from mag_tools.model.log_type import LogType
from typing import Any, Dict, List, Optional, Tuple, Type

from mag_db.bean.db_list import DbList
from mag_db.bean.db_page import DbPage
from mag_db.data.db_output import DbOutput
from mag_db.data.result_set_helper import ResultSetHelper
from mag_db.sql.base_executor import BaseExecutor


class QueryExecutor(BaseExecutor):
    def get_count(self) -> int:
        raise NotImplementedError("Subclasses should implement this method")

    def check(self) -> None:
        raise NotImplementedError("Subclasses should implement this method")

    def execute(self, bean_class: Type, column_name_map: Dict[str, str] = None) -> Any:
        beans = self.execute_beans(bean_class, column_name_map)
        return beans[0] if beans else None

    def execute_beans(self, bean_cls: Type, column_name_map: Dict[str, str] = None) -> List[Any]:
        result_set = self.__fetchall()

        output = DbOutput.from_class(bean_cls, self._column_names, column_name_map)
        output.set_multi_table(len(self._tables) > 1)
        return ResultSetHelper.to_beans(result_set, output)

    def execute_beans_by_page(self, bean_cls: Type, column_name_map: Dict[str, str] = None, page: Optional[DbPage] = None) -> DbList:
        result_set = self.__fetchall(page)
        total_count = self.get_count()

        output = DbOutput.from_class(bean_cls, self._column_names, column_name_map)
        output.set_multi_table(len(self._tables) > 1)

        data = ResultSetHelper.to_beans(result_set, output)
        return DbList(data, page, total_count)

    def execute_map(self)->Dict[str, Any]:
        maps = self.execute_maps()
        return maps[0] if maps else {}

    def execute_maps(self)-> List[Dict[str, Any]]:
        output = DbOutput.from_class(None, self._column_names)
        result_set = self.__fetchall()

        return ResultSetHelper.to_maps(result_set, output)

    def execute_maps_by_page(self, page: Optional[DbPage]= None)-> DbList:
        result_set = self.__fetchall(page)
        total_count = self.get_count()

        output = DbOutput.from_class(Dict, self._column_names)
        data = ResultSetHelper.to_maps(result_set, output)
        return DbList(data, page, total_count)

    def __fetchall(self, page: Optional[DbPage] = None) -> Tuple[Tuple[Any,...],...]:
        self.check()

        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"{self._sql} {page.get_sql()}" if page else self._sql)
                    return cursor.fetchall()
        except pymysql.MySQLError as e:
            Logger.throw(LogType.DAO, f"查询时出错: {self._sql}")