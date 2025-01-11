from dataclasses import dataclass


@dataclass
class PrimaryKey:
    column_name: str
    key_seq: int
    pk_name: str
    increment: bool

    def __init__(self, column_name: str, key_seq: int, pk_name: str, increment: bool):
        """
        主键的Bean类

        :param column_name: 列名
        :param key_seq: 主键序号
        :param pk_name: 主键名
        :param increment: 是否自增长
        """
        self.column_name = column_name
        self.key_seq = key_seq
        self.pk_name = pk_name
        self.increment = increment

    def __str__(self):
        return f"PrimaryKey(column_name={self.column_name}, key_seq={self.key_seq}, pk_name={self.pk_name}, increment={self.increment})"