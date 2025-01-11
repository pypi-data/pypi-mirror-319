import unittest
from unittest.mock import MagicMock, patch
from typing import TypeVar


from mag_db.core.simple_dao import SimpleDao
from builder.where import Where

T = TypeVar('T')

class Test:
    def __init__(self, id_: int, name: str) -> None:
        self.id_ = id_
        self.name = name

class TestDao(SimpleDao):
    def __init__(self):
        super().__init__('test_table', Test)


class TestSimpleDao(unittest.TestCase):
    @patch('sql.index_query_executor.IndexQueryExecutor.execute')
    @patch('mag_db.core.base_dao.BaseDao._session', new_callable=MagicMock)
    @patch('mag_db.core.base_dao.BaseDao._table', new_callable=MagicMock)
    def test_query(self, mock_table, mock_session, mock_execute):
        # mock_execute.return_value = MagicMock()
        dao = TestDao()
        where = Where()

        result = dao.query(Test, where)
        print(result)

        # self.assertIsNotNone(result)
        # mock_execute.assert_called_once_with(bean_class, mock_table.get_column_names_mapping())

if __name__ == '__main__':
    unittest.main()
