from typing import List

from mag_tools.exception.dao_exception import DaoException
from mag_tools.log.logger import Logger
from mag_tools.model.log_type import LogType
from mag_tools.model.symbol import Symbol

from mag_db.core.db_session import DBSession
from mag_db.data.index_parameters import IndexParameters
from mag_db.sql.query_excutor import QueryExecutor
from mag_db.utils.dao_utils import DaoUtils


class IndexQueryExecutor(QueryExecutor):
    def __init__(self, sql: str, session: DBSession):
        super().__init__(sql, session)

        self.index_parameters = IndexParameters()

    def prepare(self):
        parameters_setter = self.index_parameters.get_parameters_setter()
        return parameters_setter.get_values()

    def clear_parameters(self) -> None:
        self.index_parameters = None

    def set_string(self, parameter: str) -> None:
        self.index_parameters.set_string(parameter)

    def set_bytes(self, parameter: bytes) -> None:
        self.index_parameters.set_bytes(parameter)

    def set_date(self, parameter) -> None:
        self.index_parameters.set_date(parameter)

    def set_time(self, parameter) -> None:
        self.index_parameters.set_time(parameter)

    def set_datetime(self, parameter) -> None:
        self.index_parameters.set_datetime(parameter)

    def set_bool(self, parameter: bool) -> None:
        self.index_parameters.set_bool(parameter)

    def set_list(self, params: List) -> None:
        self.index_parameters.set_list(params)

    def check(self) -> None:
        number_of_holder = self._sql.count(Symbol.PLACE_HOLDER.code)
        if number_of_holder != self.index_parameters.parameter_count:
            params = ", ".join(map(str, self.index_parameters.parameters))
            msg = f"参数个数不匹配(占位符数={number_of_holder}, 参数个数={self.index_parameters.parameter_count})\n参数为：{params}"
            Logger.throw(LogType.DAO, msg)

    def get_count(self) -> int:
        count = 0
        try:
            count_sql = DaoUtils.get_count_sql(self._sql)

            query_executor = IndexQueryExecutor(count_sql, self._session)
            query_executor.index_parameters = self.index_parameters
            record = query_executor.execute_map()
            count = record.get("COUNT(*) AS COUNT_")
        except DaoException as dao:
            Logger.info(LogType.DAO, dao)
        return count
