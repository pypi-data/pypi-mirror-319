import unittest

from mag_db.bean.table import Table
from mag_db.utils.sql_parser import SqlParser


class TestSqlParser(unittest.TestCase):

    def test_get_tables(self):
        sql = "SELECT * FROM test_table"
        expected_tables = ["test_table"]
        self.assertEqual([table.name for table in SqlParser.get_tables(sql)], expected_tables)

        sql = "INSERT INTO test_table (col1, col2) VALUES (1, 2)"
        expected_tables = ["test_table"]
        self.assertEqual([table.name for table in SqlParser.get_tables(sql)], expected_tables)

        sql = "UPDATE test_table SET col1 = 1 WHERE col2 = 2"
        expected_tables = ["test_table"]
        self.assertEqual([table.name for table in SqlParser.get_tables(sql)], expected_tables)

        sql = "DELETE FROM test_table WHERE col1 = 1"
        expected_tables = ["test_table"]
        self.assertEqual([table.name for table in SqlParser.get_tables(sql)], expected_tables)

    def test_get_column_names(self):
        sql = "SELECT col1, col2 FROM test_table"
        expected_columns = ["col1", "col2"]
        self.assertEqual(SqlParser.get_column_names(sql), expected_columns)

        sql = "INSERT INTO test_table (col1, col2) VALUES (1, 2)"
        expected_columns = ["col1", "col2"]
        self.assertEqual(SqlParser.get_column_names(sql), expected_columns)

        sql = "UPDATE test_table SET col1 = 1, col2 = 2 WHERE col3 = 3"
        expected_columns = ["col1", "col2"]
        self.assertEqual(SqlParser.get_column_names(sql), expected_columns)

    def test_convert_column_name(self):
        sql = "SELECT t.col1, t.col2 FROM test_table AS t"
        tables = [Table(name= "test_table", alias= "t")]
        expected_sql = "SELECT test_table.col1, test_table.col2 FROM test_table AS t"
        self.assertEqual(SqlParser.convert_column_name(sql, tables), expected_sql)

    def test_delimit_to_array(self):
        sql = "SELECT col1, col2 FROM test_table"
        expected_array = ["SELECT", "col1,", "col2", "FROM", "test_table"]
        self.assertEqual(SqlParser.delimit_to_array(sql), expected_array)

if __name__ == '__main__':
    unittest.main()
