from datetime import date, datetime, time
from enum import Enum
from typing import List, Dict, TypeVar, Generic, Any
from dataclasses import dataclass, field

from mag_tools.model.base_enum import BaseEnum
from mag_tools.utils.common.string_utils import StringUtils

from mag_db.data.parameter_setter import ParameterSetter
from mag_db.handler.type_constant import TypeConstant
from mag_db.handler.type_handler import TypeHandler
from mag_db.handler.type_handler_factory import TypeHandlerFactory
from mag_db.utils.column_utils import ColumnUtils
from mag_db.utils.dao_utils import DaoUtils

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

@dataclass
class IndexParameters:
    __parameters: List[Any] = field(default_factory=list)
    __type_handlers: List[TypeHandler] = field(default_factory=list)

    def set_string(self, parameter: str) -> None:
        self.__set_parameter(parameter, TypeConstant.STRING)

    def set_bytes(self, parameter: bytes) -> None:
        self.__set_parameter(parameter, TypeConstant.BYTES)

    def set_int(self, parameter: int) -> None:
        self.__set_parameter(parameter, TypeConstant.INT)

    def set_float(self, parameter: float) -> None:
        self.__set_parameter(parameter, TypeConstant.FLOAT)

    def set_decimal(self, parameter: float) -> None:
        self.__set_parameter(parameter, TypeConstant.DECIMAL)

    def set_date(self, parameter: date) -> None:
        self.__set_parameter(parameter, TypeConstant.DATE)

    def set_time(self, parameter: time) -> None:
        self.__set_parameter(parameter, TypeConstant.TIME)

    def set_datetime(self, parameter: datetime) -> None:
        self.__set_parameter(parameter, TypeConstant.DATETIME)

    def set_bool(self, parameter: bool) -> None:
        self.__set_parameter(parameter, TypeConstant.BOOL)

    def set_bean(self, param_bean: T, column_names: List[str]) -> None:
        field_names = [ColumnUtils.to_bean_field_name(column_name) for column_name in column_names]
        self.__put_bean(param_bean, field_names)

    def set_beans(self, param_beans: List[T], column_names: List[str]) -> None:
        if param_beans:
            field_names = [ColumnUtils.to_bean_field_name(column_name) for column_name in column_names]
            for param_bean in param_beans:
                self.__put_bean(param_bean, field_names)

    def set_field_map(self, field_map: Dict[K, V], column_names: List[str]) -> None:
        field_names = [ColumnUtils.to_bean_field_name(column_name) for column_name in column_names]
        self.__put_map(field_map, field_names)

    def set_field_maps(self, field_maps: List[Dict[K, V]], column_names: List[str]) -> None:
        if field_maps:
            field_names = [ColumnUtils.to_bean_field_name(column_name) for column_name in column_names]
            for field_map in field_maps:
                self.__put_map(field_map, field_names)

    def set_list(self, params: List[T]) -> None:
        if not params:
            return

        for param in params:
            if isinstance(param, Enum):
                value = param.code if isinstance(param, BaseEnum) else param.name
                self.__set_parameter(value, TypeHandlerFactory.get(value.__class__))
            else:
                self.__set_parameter(param, TypeHandlerFactory.get(param.__class__) if param else None)

    @property
    def parameter_count(self) -> int:
        return len(self.__parameters)

    @property
    def parameters(self):
        return self.__parameters

    @property
    def type_handlers(self):
        return self.__type_handlers

    def get_parameters_setter(self) -> ParameterSetter:
        parameter_setter = ParameterSetter()

        for i, parameter in enumerate(self.__parameters):
            type_handler = self.__type_handlers[i]
            type_handler.set_parameter(parameter_setter, parameter)

        return parameter_setter

    def __set_parameter(self, parameter: Any, type_handler: TypeHandler) -> None:
        self.__parameters.append(parameter)
        self.__type_handlers.append(type_handler)

    def __put_bean(self, param_bean: T, column_names: List[str]) -> None:
        for column_name in column_names:
            bean_field_name = StringUtils.hump2underline(column_name)

            try:
                bean_field_value = getattr(param_bean, bean_field_name, None)
                bean_field_type = type(bean_field_value)

                if isinstance(bean_field_value, Enum):
                    bean_field_value = bean_field_value.code if hasattr(bean_field_value, 'code') else bean_field_value.name

                type_handler = DaoUtils.get_type_handler(bean_field_type)
                self.__set_parameter(bean_field_value, type_handler)
            except AttributeError:
                pass  # 该列名在bean中不存在，跳过

    def __put_map(self, field_set: Dict[str, V], column_names: List[str]) -> None:
        for column_name in column_names:
            field_value = field_set.get(column_name)
            field_type = type(field_value)
            if field_type is None:
                field_type = str

            type_handler = DaoUtils.get_type_handler(field_type)
            self.__set_parameter(field_value, type_handler)
