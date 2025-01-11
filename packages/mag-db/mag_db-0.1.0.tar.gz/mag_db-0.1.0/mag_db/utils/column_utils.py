from datetime import date, datetime
from decimal import Decimal
from enum import Enum

from mag_db.model.db_type import DbType

from mag_db.bean.column import Column
from mag_db.model.oracle_convert_type import OracleConvertType
from mag_db.model.sql_server_convert_type import SqlServerConvertType
from mag_db.model.sql_type import SqlType

from typing import Any, List


class ColumnUtils:
    MAX_OF_VARCHAR = 8 * 1024
    MAX_OF_TEXT = 64 * 1024 - 1
    MAX_OF_MEDIUM_TEXT = 16 * 1024 * 1024 - 1

    @staticmethod
    def to_bean_field_name(column_name: str) -> str:
        """
        将列名变换为bean的字段名
        注：如下列名可自动转换：
        1、列名由多个单词组成时，之间使用"_"连接，全小写字母
        2、列名与bean字段名相同
        3、列名为：表名.列名
        对第三种，去掉表名和点，再转换
        如：数据库字段：user.family_address; Bean字段名：family_address

        :param column_name: 列名，格式：列名；表名.列名；表名__列名；表名~列名，列名为首字母小写的驼峰格式或_连接的数据库格式
        :return: bean的字段名，首字母小写的驼峰格式
        """
        return Column(column_name).name if column_name else ""

    @staticmethod
    def to_columns(column_names: List[str]) -> List[Column]:
        return [Column(name) for name in column_names]

    @staticmethod
    def contains(columns: List[Column], column_name: str) -> bool:
        """
        判定列名列表中是否包含指定列名

        :param columns: 列的列表
        :param column_name: 指定的列名
        :return: 列名列表中是否包含指定列名
        """
        return any(column.name == column_name for column in columns)

    @staticmethod
    def convert_to_mysql(columns: List[Column], db_type: DbType) -> List[Column]:
        def convert_column(column: Column):
            from_type = column.sql_type

            if db_type == DbType.ORACLE:
                column.sql_type = OracleConvertType.of_code(from_type.code).sql_type
            elif db_type == DbType.SQL_SERVER:
                column.sql_type = SqlServerConvertType.of_code(from_type.code).sql_type

            if db_type == DbType.SQL_SERVER:
                if from_type == SqlType.MONEY:
                    column.decimal_digits = 4
                    column.column_size = 19
                elif from_type == SqlType.TIMESTAMP:
                    column.column_size = 64

            if column.sql_type == SqlType.VARCHAR:
                if column.column_size is None:
                    column.column_size = ColumnUtils.MAX_OF_VARCHAR
                elif column.column_size > ColumnUtils.MAX_OF_VARCHAR:
                    sql_type = SqlType.LONGTEXT if column.column_size > ColumnUtils.MAX_OF_MEDIUM_TEXT else SqlType.MEDIUMTEXT
                    column.sql_type = sql_type
                    column.column_size = 0
                    column.char_octet_length = 0
                    if column.default_value is not None:
                        column.default_value = None
            elif column.sql_type == SqlType.BIT:
                default_value = column.default_value
                if default_value is not None:
                    if default_value not in ["b'0'", "b'1'"]:
                        column.sql_type = SqlType.TINYINT
                        column.column_size = 1
                elif column.column_size == 1:
                    column.sql_type = SqlType.TINYINT
                    column.column_size = 1
            elif column.sql_type == SqlType.ENUM:
                column.sql_type = SqlType.VARCHAR
                column.column_size = 128

            return column

        return [convert_column(column) for column in columns]

    @staticmethod
    def to_column(field: Any):
        column_size = None
        decimal_digits = None

        cls = type(field)
        if cls == str:
            column_size = 255
            sql_type = SqlType.of_class(cls, column_size)
        elif cls in [float, int, Decimal]:
            sql_type = SqlType.of_class(cls, column_size)
        elif isinstance(cls, Enum):
            column_size = 32
            sql_type = SqlType.of_class(str, column_size)
        elif cls in [datetime, date]:
            sql_type = SqlType.of_class(cls)
        else:
            sql_type = SqlType.of_class(cls)

        return Column(
            name=field.name,
            sql_type=sql_type,
            column_size=column_size,
            decimal_digits=decimal_digits
        )
