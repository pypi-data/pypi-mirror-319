import unittest
from unittest.mock import patch, MagicMock

from mag_db.core.db_session import DBSession
from mag_db.core.base_dao import BaseDao

class TestBaseDao(unittest.TestCase):

    @patch('mag_db.core.db_session.DBSession.connect')
    @patch('mag_db.manager.datasource_mgr.DatasourceMgr.get_datasource')
    def setUp(self, mock_get_datasource, mock_connect):
        mock_get_datasource.return_value = MagicMock()
        mock_connect.return_value = MagicMock()
        self.dao = BaseDao()

    @patch('mag_db.core.db_session.DBSession.connect')
    def test_insert(self, mock_connect):
        mock_conn = mock_connect.return_value.__enter__.return_value
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value

        insert_sql = "INSERT INTO test_table (id, name) VALUES (12, 'value2')"
        self.dao.insert(insert_sql)

        mock_cursor.execute.assert_called_once_with(insert_sql)
        mock_conn.commit.assert_called_once()

    @patch('mag_db.core.db_session.DBSession.connect')
    def test_update(self, mock_connect):
        mock_conn = mock_connect.return_value.__enter__.return_value
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value

        update_sql = "UPDATE test_table SET id = 12 WHERE name = 'value2'"
        self.dao.update(update_sql)

        mock_cursor.execute.assert_called_once_with(update_sql)
        mock_conn.commit.assert_called_once()

    @patch('mag_db.core.db_session.DBSession.connect')
    def test_query(self, mock_connect):
        mock_conn = mock_connect.return_value.__enter__.return_value
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.description = [('id',), ('name',)]
        mock_cursor.fetchall.return_value = [(12, 'value2')]

        query_sql = "SELECT id, name FROM test_table"
        results = self.dao.query(query_sql)

        mock_cursor.execute.assert_called_once_with(query_sql)
        self.assertEqual(results, [{'id': 12, 'name': 'value2'}])

    @patch('mag_db.core.db_session.DBSession.connect')
    def test_delete(self, mock_connect):
        mock_conn = mock_connect.return_value.__enter__.return_value
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value

        delete_sql = "DELETE FROM test_table WHERE id = 12"
        self.dao.delete(delete_sql)

        mock_cursor.execute.assert_called_once_with(delete_sql)
        mock_conn.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
