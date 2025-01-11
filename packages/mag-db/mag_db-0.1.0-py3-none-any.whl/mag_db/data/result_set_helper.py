from typing import Any, Dict, List, Tuple

from mag_db.data.db_output import DbOutput


class ResultSetHelper:
    @staticmethod
    def to_maps(result_set: Tuple[Tuple[Any, ...], ...], db_output: DbOutput) -> List[Dict[str, Any]]:
        return [
            {
                db_output.column_name_mapping.get_target_name(column_name) or column_name:
                    row[idx] for idx, column_name in enumerate(db_output.column_names)
            }
            for row in result_set
        ]

    @staticmethod
    def to_beans(result_set: Tuple[Tuple[Any,...],...], db_output: DbOutput) -> List[Any]:
        result_list = []
        for row in result_set:
            bean = db_output.result_class()
            for idx, column_name in enumerate(db_output.column_names):
                target_name = db_output.column_name_mapping.get_target_name(column_name)
                if target_name is None:
                    target_name = column_name
                setattr(bean, target_name, row[idx])
            result_list.append(bean)

        return result_list
