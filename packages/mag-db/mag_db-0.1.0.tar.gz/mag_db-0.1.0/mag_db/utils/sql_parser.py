from typing import List, Optional
import sqlparse
from sqlparse.sql import Function, Identifier, Token
from sqlparse.tokens import Name

from mag_db.bean.table import Table
from mag_db.model.operator_type import OperatorType


class SqlParser:
    """
    SQL解析工具类

    作者: xlcao
    版本: 1.0
    版权所有: Copyright (c) 2018 by Xiaolong Cao. All rights reserved.
    创建日期: 2018/6/28
    """

    @staticmethod
    def get_tables(sql: str) -> List[Table]:
        tables = []

        if sql:
            # LOAD DATA是MYSQL特有，其它SQL并不支持
            if "LOAD DATA" in sql.upper():
                return SqlParser.__parse_load_data(sql)

            parsed = sqlparse.parse(sql)
            stmt = parsed[0]

            if stmt.get_type() == 'SELECT':
                tables = SqlParser.__get_query_tables(sql)
            elif stmt.get_type() in ('UPDATE', 'INSERT', 'DELETE'):
                for token in stmt.tokens:
                    if isinstance(token, Identifier):
                        tables.append(Table.of_whole_name(token.get_real_name()))
                    elif isinstance(token, Token) and token.ttype == Name:
                        tables.append(Table.of_whole_name(token.value))
                    elif isinstance(token, Function):
                        tables.append(Table.of_whole_name(token.value))

        return tables

    @staticmethod
    def get_column_names(sql: str) -> List[str]:
        db_params = []

        sql = sql.strip()
        up_sql = sql.upper()

        # SELECT DISTINCT
        if up_sql.startswith("SELECT DISTINCT"):
            begin = up_sql.find("SELECT DISTINCT ") + len("SELECT DISTINCT ")
            end = up_sql.find(" FROM ")
            if begin >= 0 and end > 0:
                str_params = sql[begin:end]
                db_params = str_params.split(", ")
        # SELECT
        elif up_sql.startswith("SELECT"):
            begin = up_sql.find("SELECT ") + len("SELECT ")
            end = up_sql.find(" FROM ")
            if begin >= 0 and end > 0:
                str_params = sql[begin:end]
                db_params = str_params.split(", ")
        # INSERT INTO
        elif up_sql.startswith("INSERT INTO"):
            begin = up_sql.find("(")
            end = up_sql.find(")")
            if begin > 0 and end > 0:
                str_params = sql[begin + 1:end]
                db_params = str_params.split(", ")
        # UPDATE
        elif up_sql.startswith("UPDATE"):
            begin = up_sql.find(" SET ") + len(" SET ")
            end = up_sql.find(" WHERE ")
            if begin > 0 and end > 0:
                str_params = sql[begin:end]
                param_list = str_params.split(", ")
                for param in param_list:
                    idx = param.find("=")
                    if idx > 0:
                        db_param = param[:idx].strip()
                        db_params.append(db_param)

        return db_params

    @staticmethod
    def convert_column_name(sql: str, tables: List[Table]) -> str:
        # LOAD DATA是MYSQL特有，其它SQL并不支持
        if "LOAD DATA" in sql.upper():
            return sql

        for table in tables:
            table_name = table.name
            alias = table.alias

            # 列名中含有表别名的，则替换为表名
            if alias:
                # 别名格式为：AS abc
                # 去掉AS
                if "AS " in alias:
                    alias = alias.replace("AS ", "")

                if "." in sql:
                    # 处理表别名.列名的情况
                    sql = sql.replace(alias, table_name)

                    # 处理表别名.列名的情况，当列别名为空时，会自动设置表别名.列名作为列别名
                    sql = sql.replace(alias, table_name)
                else:
                    sql = sql.replace(f" {alias}.", f" {table_name}.")
                    sql = sql.replace(f",{alias}.", f",{table_name}.")
                    sql = sql.replace(f"({alias}.", f"({table_name}.")
                    sql = sql.replace(f"={alias}.", f"={table_name}.")
                    sql = sql.replace(f">{alias}.", f">{table_name}.")
                    sql = sql.replace(f"<{alias}.", f"<{table_name}.")

                    # 去掉表别名设置，表别名在表名后，空格分隔，后面为空格或逗号
                    sql = sql.replace(f" {alias},", ",")
                    sql = sql.replace(f" {alias} ", " ")

        return sql

    @staticmethod
    def delimit_to_array(sql: str) -> List[str]:
        list_ = []

        sql = sql.strip()
        while " " in sql:
            idx = sql.find(" ")
            # 首字符不为小括号
            if sql[0] not in ('(', ')'):
                # 首字符不为引号，则将空格前内容保存
                if sql[0] not in ('\'', '"'):
                    list_.append(sql[:idx])
                    sql = sql[idx + 1:].strip()
                # 首字符为引号时，将引号内容保存，如引号不匹配，则将空格前作为整体保存
                else:
                    pair = SqlParser.__find_match_quote(sql, sql[0])
                    if pair:
                        list_.append(sql[pair[0]:pair[1] + 1])
                        sql = sql[pair[1] + 1:].strip()
                    else:
                        list_.append(sql[:idx])
                        sql = sql[idx + 1:].strip()
            # 首字符为小括号时，截取保存后继续
            else:
                list_.append(sql[0])
                sql = sql[1:].strip()

        if sql:
            list_.append(sql)

        # 将SQL语句中的关键词转为大写
        array = list_
        for i in range(len(array)):
            if SqlParser.__is_keyword(array[i]):
                array[i] = array[i].upper()
        return array

    @staticmethod
    def __get_query_tables(sql: str) -> List[Table]:
        tables = []

        up_sql = sql.upper()
        if OperatorType.SELECT.code in up_sql:
            begin = sql.find(OperatorType.FROM.code)
            if begin > 0:
                # IN语句紧跟在FROM后面，中间没有其它的关键字
                end = sql.find(OperatorType.IN.code)

                # WHERE语句紧跟在FROM后面，中间没有其它的关键字
                idx_where = sql.find(OperatorType.WHERE.code)
                if end == -1 or (begin < idx_where < end):
                    end = idx_where

                # GROUP BY语句紧跟在FROM后面，中间没有其它的关键字
                idx_group = sql.find(OperatorType.GROUP_BY.code)
                if end == -1 or (begin < idx_group < end):
                    end = idx_group

                # ORDER BY语句紧跟在FROM后面，中间没有其它的关键字
                idx_order = sql.find(OperatorType.ORDER_BY.code)
                if end == -1 or (begin < idx_order < end):
                    end = idx_order

                # HAVING语句紧跟在FROM后面，中间没有其它的关键字
                idx_having = sql.find(OperatorType.HAVING.code)
                if end == -1 or (begin < idx_having < end):
                    end = idx_having

                # 查询子语句,(紧跟在FROM后面，与FROM之间不会有表名
                sub_sql = sql.find(" (", begin)
                if end == -1 or (begin < sub_sql < end):
                    end = sub_sql

                if end < begin + 4:
                    str_table_name = sql[begin + 4:]
                else:
                    str_table_name = sql[begin + 4:end]

                table_name_list = str_table_name.split(", ")
                for whole_table_name in table_name_list:
                    table = Table.of_whole_name(whole_table_name)
                    tables.append(table)

        return tables

    @staticmethod
    def __is_keyword(str_: str) -> bool:
        keywords = ["INSERT", "UPDATE", "DELETE", "SELECT", "NOT", "LIKE", "WHERE", "FROM", "IN", "AS", "BY", "GROUP", "ORDER", "COUNT", "ALIAS"]
        return str_ is not None and str_.upper() in keywords

    @staticmethod
    def __parse_load_data(sql: str) -> List[Table]:
        sql = sql.split("INTO TABLE")[1].strip()
        table_name = sql.split(" ")[0].strip()
        return [Table.of_whole_name(table_name)]

    @staticmethod
    def __find_match_quote(sql: str, quote: str) -> Optional[tuple]:
        start = sql.find(quote)
        end = sql.find(quote, start + 1)
        if start != -1 and end != -1:
            return start, end
        return None