from typing import List, Optional, Type, TypeVar, Generic

from mag_tools.bean.easy_map import EasyMap
from mag_tools.exception.dao_exception import DaoException
from mag_tools.utils.common.list_utils import ListUtils

from builder.insert import Insert
from builder.select import Select
from builder.where import Where
from mag_db.core.base_dao import BaseDao
from manager.datasource_mgr import DatasourceMgr
from sql.index_query_executor import IndexQueryExecutor

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class SimpleDao(BaseDao):
    _table = None

    def __init__(self, table_name: str, bean_type: Type = None, column_names: List[str] = None, distinct: bool = False):
        super().__init__()

        self._table.name = table_name
        self._table.distinct = distinct

        if column_names:
            self._table.column_names = column_names
        elif bean_type and hasattr(bean_type, '__annotations__'):
            self._table.column_names = list(bean_type.__annotations__.keys())
        else:
            self._table.column_names = []
    """
    常用的DAO操作类

          @version 1.0
          @Description 提供基本数据库操作, 如插入、更新等。
          注：SimpleDao类只提供简单的单表数据库操作，对复杂的SQL或多表操作需继承BaseDao来完成。
          <p>
          数据源名称，其值必须与配置文件DBConfig.xml中的某个数据源名称一致。DBConfig.xml中可以定义多个数据源，
          但每个Dao基类只能对应其中一个数据源。数据源名称应当常量定义,以便事务处理使用。
          <p>
          Copyright: Copyright (c) 2015
          Company:
    """

    # def insert(self, bean: T) -> int:
    #     """
    #      插入一条记录
    #      表名通过Dao类@Table注解设置；列名通过Dao类@Table和方法@DbInsert注解设置
    #
    #      @param bean 要插入的数据
    #      @param <T>   列数值Bean类型
    #      @throws DaoException 异常
    #     """
    #     if isinstance(bean, list):
    #         raise DaoException("该方法只能插入单条数据")
    #
    #     ret = self.insert_beans([bean])
    #     return ret[0] if ret else None
    #
    # def insert_field_set(self, field_set: 'IFieldSet[K, V]') -> int:
    #     """
    #     插入操作
    #     表名通过Dao类@Table注解设置；列名通过Dao类@Table和方法@DbInsert注解设置"""
    #     ret = self.insert_field_sets([field_set])
    #     return ret[0] if ret else None

    # def insert_beans(self, beans: List[T]) -> List[int]:
    #     """
    #     多记录插入操作
    #     表名通过Dao类@Table注解设置；列名通过Dao类@Table和方法@DbInsert注解设置"""
    #     return self.do_insert_beans(beans)
    #
    # def insert_beans_set(self, beans: set) -> List[int]:
    #     """
    #     多记录插入操作
    #     表名通过Dao类@Table注解设置；列名通过Dao类@Table和方法@DbInsert注解设置"""
    #     return self.do_insert_beans(list(beans))

    # @Schema(description="""
    #         多记录插入操作
    #         表名通过Dao类@Table注解设置；列名通过Dao类@Table和方法@DbInsert注解设置""")
    # @LogHandler(type=DaoLog, value="插入操作失败")
    # def insert_field_sets(self, field_sets: List['IFieldSet[K, V]']) -> List[int]:
    #     return self.do_insert_field_sets(field_sets)
    #
    # @Schema(description="""
    #         更新操作
    #              表名通过Dao类@Table注解设置；列名通过Dao类@Table和方法@DbUpdate注解设置""")
    # @LogHandler(type=DaoLog, value="根据主键更新操作失败")
    # @Deprecated
    # def update_params(self, params: List[T], where: Where) -> int:
    #     update_sql = UpdateUtils.get_from_annotation(self.dao_caller(), None, where)
    #
    #     update = self.dao_creator().create_update(update_sql.to_string())
    #     update.set_list(params)
    #     if where.has_fields():
    #         update.set_list(where.get_fields())
    #
    #     return update.execute()
    #
    # @Schema(description="""
    #         根据主键更新多个Bean
    #              表名通过Dao类@Table注解设置；列名通过Dao类@Table和方法@DbUpdate注解设置""")
    # @LogHandler(type=DaoLog, value="根据主键更新操作失败")
    # @Transact
    # def update_beans(self, param_beans: List[T]) -> int:
    #     num = 0
    #     for bean in param_beans:
    #         num += self.update_by_id(bean)
    #     return num
    #

    def query(self, bean_class: type, where: Where) -> T:
        """
        查询数据库符合条件的指定记录
        """
        select = self.__get_select(where)

        query = IndexQueryExecutor(select.__str__(), self._session)
        if where.has_fields():
            query.set_list(where.fields)

        return query.execute(bean_class, self._table.get_column_names_mapping())
    #
    # @Schema(description="""
    #         查询数据库，查询结果保存在一个IRecord
    #            表名通过Dao类@Table注解设置，列名通过Dao类@Table注解及方法@DbQuery注解共同设置，查询条件和参数通过方法变量传入""")
    # @LogHandler(type=DaoLog, value="查询数据库操作失败")
    # def query_record(self, where: Where) -> 'IRecord':
    #     select = QueryUtils.get_from_annotation(self.dao_caller(), where)
    #
    #     query = self.dao_creator().create_query(select.to_string())
    #     if where.has_fields():
    #         query.set_list(where.get_fields())
    #
    #     return query.execute_record()
    #
    # @Schema(description="""
    #         根据主键查询符合条件的指定记录
    #            表名通过Dao类@Table注解设置，列名通过Dao类@Table注解及方法@DbQuery注解共同设置""")
    # @LogHandler(type=DaoLog, value="根据主键查询操作失败")
    # def query_by_id(self, bean_class: type, id: object) -> T:
    #     where = Where.builder().column(self.dao_caller().get_primary_key(), Relation.EQUAL, id)
    #     return self.query(bean_class, where)
    #
    # @Schema(description="""
    #         根据主键查询
    #             表名通过Dao类@Table注解设置，列名通过Dao类@Table注解及方法@DbQuery注解共同设置
    #         """)
    # @LogHandler(type=DaoLog, value="根据主键查询操作失败")
    # def query_record_by_id(self, id: object) -> 'IRecord':
    #     where = Where.builder().column(self.dao_caller().get_primary_key(), Relation.EQUAL, id)
    #     return self.query_record(where)
    #
    # @Schema(description="""
    #         按条件列表数据库记录
    #              表名通过Dao类@Table注解设置，列名通过Dao类@Table注解及方法@DbQuery注解共同设置，查询条件和参数通过方法变量传入
    #         """)
    # @LogHandler(type=DaoLog, value="按条件列表数据库操作失败")
    # def list(self, bean_class: type, where: Where) -> 'DbList[T]':
    #     select = QueryUtils.get_from_annotation(self.dao_caller(), where)
    #
    #     query = self.dao_creator().create_query(select.to_string())
    #     if where.has_fields():
    #         query.set_list(where.get_fields())
    #
    #     if where.is_page_query():
    #         return query.execute_list(bean_class, where.get_page(), self.dao_caller().get_column_names_mapping())
    #     else:
    #         return query.execute_list(bean_class, self.dao_caller().get_column_names_mapping())
    #
    # @LogHandler(type=DaoLog, value="按条件列表数据库操作失败")
    # def list_records(self, where: Where) -> 'DbList[IRecord]':
    #     select = QueryUtils.get_from_annotation(self.dao_caller(), where)
    #
    #     query = self.dao_creator().create_query(select.to_string())
    #     if where.has_fields():
    #         query.set_list(where.get_fields())
    #
    #     if where.is_page_query():
    #         return query.execute_record_list(where.get_page())
    #     else:
    #         return query.execute_record_list()
    #
    # @Schema(description="""
    #         列表数据库的全部记录
    #              表名通过Dao类@Table注解设置，列名通过Dao类@Table注解及方法@DbQuery注解共同设置""")
    # @LogHandler(type=DaoLog, value="查询全部结果操作失败")
    # def list_all(self, bean_class: type) -> 'DbList[T]':
    #     select = QueryUtils.get_from_annotation(self.dao_caller())
    #     query = self.dao_creator().create_query(select.to_string())
    #
    #     return query.execute_list(bean_class, self.dao_caller().get_column_names_mapping())
    #
    # @LogHandler(type=DaoLog, value="查询全部结果操作失败")
    # def list_all_records(self) -> 'DbList[IRecord]':
    #     select = QueryUtils.get_from_annotation(self.dao_caller())
    #     query = self.dao_creator().create_query(select.to_string())
    #
    #     return query.execute_record_list()
    #
    #
    # @Schema(description="查询表中最新记录的时间字段")
    # @LogHandler(type=DaoLog, value="查询表中最新记录的时间字段失败")
    # def get_latest_time(self, where: Where, order_by: str) -> datetime:
    #     if where is None:
    #         where = Where()
    #     where.order(False, order_by).limit(1)
    #
    #     record = self.query_record(where)
    #     return record.get_local_date_time(order_by)

    # def do_insert_beans(self, beans: List[T]) -> List[int]:
    #     """
    #     多记录插入操作
    #     当要插入的数据记录过多时，则分批插入
    #     @return 如有自增的主键，则返回主键值列表；否则返回null"""
    #     ret = []
    #
    #     if not beans:
    #         return ret
    #
    #     blocks = ListUtils.split(beans, int(self.datasource.max_insert))
    #
    #     insert_sql = Insert(self.table_names, self.column_names, )
    #     insert = self.dao_creator().create_insert(insert_sql.to_string())
    #     column_names_mapping = self.dao_caller().get_column_names_mapping()
    #
    #     for i, block in enumerate(blocks):
    #         if i == len(blocks) - 1:
    #             insert_sql = InsertUtils.get_from_annotation(self.dao_caller(), block[0], len(block))
    #             insert = self.dao_creator().create_insert(insert_sql.to_string())
    #
    #         ret.extend(self.insert_part_of_beans(insert, block, column_names_mapping))
    #
    #     return ret

    # def do_insert_field_sets(self, field_sets: List[EasyMap[K, V]]) -> List[int]:
    #     """
    #                 多记录插入操作
    #                 当要插入的数据记录过多时，则分批插入
    #                 @return 如有自增的主键，则返回主键值列表；否则返回null"""
    #     ret = []
    #
    #     blocks = ListUtil.split(field_sets, int(self.dao_creator().get_data_source().get_max_insert()))
    #     insert_sql = InsertUtils.get_from_annotation(self.dao_caller(), blocks[0][0], len(blocks[0]))
    #     insert = self.dao_creator().create_insert(insert_sql.to_string())
    #     column_names_mapping = self.dao_caller().get_column_names_mapping()
    #
    #     for i, block in enumerate(blocks):
    #         if i == len(blocks) - 1:
    #             insert_sql = InsertUtils.get_from_annotation(self.dao_caller(), block[0], len(block))
    #             insert = self.dao_creator().create_insert(insert_sql.to_string())
    #
    #         ret.extend(self.insert_part_of_field_sets(insert, block, column_names_mapping))
    #
    #     return ret
    #
    # def insert_part_of_beans(self, insert: 'IndexInsert', beans: List[T], column_names_mapping: dict) -> List[int]:
    #     if not beans:
    #         raise DaoException("至少要插入一条记录")
    #
    #     insert.clear_parameters()
    #     for bean in beans:
    #         insert.set_bean(bean, column_names_mapping)
    #
    #     keys = insert.execute(self.dao_caller().is_auto_increment_key())
    #
    #     if len(keys) == len(beans):
    #         for i, bean in enumerate(beans):
    #             try:
    #                 field = AnnotationUtilsEx.get_field_by_annotation(bean, PrimaryKey)
    #                 if field:
    #                     if field.get_type() == int:
    #                         FieldUtils.set_field_value(bean, field.get_name(), int(keys[i]))
    #                     elif field.get_type() == int:
    #                         FieldUtils.set_field_value(bean, field.get_name(), keys[i])
    #             except (AppException, NoSuchFieldException, InvocationTargetException, IllegalAccessException):
    #                 pass
    #
    #     return keys
    #
    # def insert_part_of_field_sets(self, insert: 'IndexInsert', field_sets: List['IFieldSet[K, V]'], column_names_mapping: dict) -> List[int]:
    #     if not field_sets:
    #         raise DaoException("至少要插入一条记录")
    #
    #     insert.clear_parameters()
    #     for field_set in field_sets:
    #         insert.set_field_set(field_set, column_names_mapping)
    #
    #     keys = insert.execute(self.dao_caller().is_auto_increment_key())
    #
    #     for i, field_set in enumerate(field_sets):
    #         try:
    #             field = AnnotationUtilsEx.get_field_by_annotation(field_set, PrimaryKey)
    #             if field:
    #                 if field.get_type() == int:
    #                     FieldUtils.set_field_value(field_set, field.get_name(), int(keys[i]))
    #                 elif field.get_type() == int:
    #                     FieldUtils.set_field_value(field_set, field.get_name(), keys[i])
    #         except (AppException, NoSuchFieldException, InvocationTargetException, IllegalAccessException):
    #             pass
    #
    #     return keys

    def __get_select(self, where: Optional[Where]) -> Select:
        select = Select(self._table.table_names, self._table.column_names, where)
        if self._table.distinct:
            select.set_distinct()
        return select
