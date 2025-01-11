from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

from mag_db.bean.column import Column
from mag_db.model.operator_type import OperatorType

@dataclass
class Table:
    sn: Optional[int] = None  # 表序号，主键
    schema_name: Optional[str] = None  # 表模式名
    name: Optional[str] = None  # 表名
    table_type: str = "TABLE"  # 表类型名
    db_sn: Optional[int] = None  # 库序号
    db_name: Optional[str] = None  # 库名
    ds_name: Optional[str] = None  # 数据源名
    __alias: Optional[str] = None  # 表别名
    primary_keys: str = ""  # 表的主键清单，逗号分开
    auto_increment: int = 0  # 自增长序号的起始值
    __columns: List[Column] = field(default_factory=list)  # 列名清单
    column_names_mapping: Dict[str, str] = field(default_factory=dict) # 列名与字段名映射表
    create_time: Optional[datetime] = None  # 创建时间
    comment: Optional[str] = None  # 描述

    def __init__(self, name: Optional[str] = None, sn: Optional[int] = None, schema_name: Optional[str] = None,
                 table_type: str = "TABLE", db_sn: Optional[int] = None, db_name: Optional[str] = None,
                 ds_name: Optional[str] = None, __alias: Optional[str] = None, primary_keys: str = "",
                 auto_increment: int = 0, columns: List[Column] = None, create_time: Optional[datetime] = None,
                 comment: Optional[str] = None):
        self.name = name
        self.sn = sn
        self.schema_name = schema_name
        self.table_type = table_type
        self.db_sn = db_sn
        self.db_name = db_name
        self.ds_name = ds_name
        self.__alias = __alias
        self.primary_keys = primary_keys
        self.auto_increment = auto_increment
        self.set_columns(columns)
        self.create_time = create_time
        self.comment = comment

    @staticmethod
    def of_whole_name(whole_name: str, schema_name: Optional[str] = None):
        table = Table()
        if whole_name:
            table.set_name(whole_name)
        if schema_name:
            table.schema_name = schema_name
        return table

    def set_name(self, table_name: str):
        """
        设置表名，完整格式为：表名 AS 别名
        :param table_name: 表名
        """
        if table_name:
            # 清除前后空格
            self.name = table_name.strip()
            sep = None

            idx = self.name.find(f" {OperatorType.AS.value} ")
            # 表名与别名之间有AS
            if idx > 0:
                sep = f" {OperatorType.AS.value} "
            else:
                idx = self.name.find(" ")
                if idx > 1:
                    sep = " "

            if sep:
                self.__alias = self.name[idx + len(sep):].strip()
                self.name = self.name[:idx].strip()

    @property
    def alias(self) -> str:
        """
        获取列别名
        :return: 列别名
        """
        if not self.__alias and self.name:
            self.__alias = f"{self.name}__{self.name}"
        return self.__alias

    def get_fully_name(self, has_alias: bool = True) -> str:
        """
        取完整表名
        :param has_alias: 是否含别名
        :return: 表名 AS 别名
        """
        if not self.name:
            return ""

        fully_name = self.name
        if has_alias and self.alias:
            fully_name += f" AS {self.alias}"
        return fully_name

    @property
    def columns(self) -> List[Column]:
        return self.__columns

    def set_columns(self, columns: List[Column]):
        """
        设置列信息
        :param columns: 列信息清单
        """
        self.__columns = []
        if columns:
            self.__columns = columns
            self.column_names_mapping = self.__get_column_names_map(columns)

            # 设置表的主键：如添加列的信息中包含了是否为主键信息，则设置表的主键
            pri_keys = [col for col in self.__columns if col.is_primary_key]
            if pri_keys:
                pri_key_strs = [col.name for col in pri_keys]
                self.primary_keys = ",".join(pri_key_strs)

    def set_sn(self, sn: int):
        """
        设置表序号
        :param sn: 表序号
        """
        self.sn = sn
        for col in self.__columns:
            col.table_sn = sn

    def set_primary_keys(self, primary_keys: str):
        """
        设置表的主键信息
        :param primary_keys: 主键清单，逗号分开
        """
        if primary_keys:
            self.primary_keys = primary_keys

            # 更新列的主键信息
            pri_key_strs = primary_keys.split(",")
            for col in self.__columns:
                if col.name in pri_key_strs:
                    col.is_primary_key = True

    def __str__(self) -> str:
        """
        流化为完整格式的字符串
        :return: 字符串
        """
        return self.get_fully_name(True)

    @property
    def is_empty(self) -> bool:
        """
        判定是否为空
        :return: 是否为空
        """
        return not self.name

    @property
    def uniques(self) -> List[Column]:
        """
        获取有唯一约束的列清单
        :return: 有唯一约束的列清单
        """
        return [col for col in self.__columns if col.is_unique()]

    def compare(self, table: 'Table') -> bool:
        """
        判定两个表是否相同
        :param table: 表信息
        :return: 是否相同
        """
        return str(self) == str(table)

    def add_column(self, column: Column):
        """
        添加列信息
        :param column: 列信息
        """
        self.__columns.append(column)

        # 如该列为主键，但表主键列表中未包含，则添加为主键
        primary_key_strs = self.primary_keys.split(",")
        if column.is_primary_key and column.name not in primary_key_strs:
            primary_key_strs.append(column.name)
            self.primary_keys = ",".join(primary_key_strs)

    def check(self):
        """
        检查表信息格式
        """
        if not self.__columns:
            self.__columns = []
        if not self.primary_keys:
            self.primary_keys = ""
        if not self.type:
            self.type = "TABLE"

        for col in self.__columns:
            if col.name in self.primary_keys:
                col.is_primary_key = True
                col.is_can_null = False
            col.table_name = self.name

    @classmethod
    def to_tables(cls, table_names: List[str]) -> List['Table']:
        """
        将表名列表转换为表的列表
        :param table_names: 表名的列表
        :return: 表的列表
        """
        return [Table(name=_name) for _name in table_names]

    @classmethod
    def __get_column_names_map(cls, columns):
        mappings = {}
        for column in columns:
            map_value = column.get_mapping()
            if map_value:
                mappings[column.get_name()] = map_value
        return mappings
