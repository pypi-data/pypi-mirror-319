from typing import Dict, List, Optional, Type

from mag_db.data.column_names_mapping import ColumnNamesMapping


class DbOutput:
    def __init__(self):
        """
        数据库输出信息类
        """
        self.start_column_index = 1
        self.result_class = None
        self.column_name_mapping = ColumnNamesMapping()
        self.is_multi_table = False
        self.column_names = []

    @classmethod
    def from_class(cls, bean_class: Optional[Type], col_names: List[str], col_name_map: Optional[Dict[str, str]] = None):
        output = cls()
        output.column_names = col_names

        if bean_class:
            mapping_from_bean = ColumnNamesMapping.get_by_bean(bean_class, col_names, col_name_map)
            output.column_name_mapping = mapping_from_bean
            output.result_class = bean_class

        return output
