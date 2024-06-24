from typing import Any
from django.db import models
from myforms import CustomMonthField
from datetime import datetime
# class MonthField(models.CharField):
#     def formfield(self, **kwargs):
#         defaults = {'form_class': CustomMonthField}
#         defaults.update(kwargs)
#         return super().formfield(**defaults)

#     # def from_db_value(self, value, expression, connection):
#     #     if value is None:
#     #         return value
#     #     print("from_db_value: ", value, type(value))
#     #     return datetime.strptime(value, '%Y-%m')
    
#     def to_python(self, value):
#         if value is None:
#             return value
#         if isinstance(value, datetime):
#             return value
#         return datetime.strptime(value, '%Y-%m')
    
#     def get_prep_value(self, value):
#         if value is None:
#             return value
#         print("get_prep_value: ", value, type(value))
#         return value
    
#     def value_to_string(self, obj):
#         value = self.value_from_object(obj)
#         return self.get_prep_value(value)
    
from django.db import models
import datetime

class MonthField(models.DateField):
    def formfield(self, **kwargs):
        defaults = {'form_class': CustomMonthField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
    
    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, datetime.date):
            return value
        # 尝试将字符串转换为date对象，假设格式为YYYY-MM
        try:
            return datetime.datetime.strptime(value, '%Y-%m').date()
        except ValueError:
            raise ValueError("请输入有效的日期格式，格式为YYYY-MM。")

    def get_prep_value(self, value):
        if value is None or value == '':
            return None
        # 确保值为date对象后，转换为YYYY-MM格式的字符串
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m')
        return value

    def from_db_value(self, value, expression, connection):
        if value is None or value == '':
            return None
        print("---from_db_value: ", value, type(value))
        # 从数据库读取的值通常是字符串，需要转换为date对象
        return datetime.datetime.strptime(value, '%Y-%m')
    
class CreateTime(models.DateTimeField):
    auto_field = True
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs['auto_now_add'] = True
        kwargs['verbose_name'] = '创建时间'
        super().__init__(*args, **kwargs)

class LastModified(models.DateTimeField):
    auto_field = True
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs['auto_now'] = True
        kwargs['verbose_name'] = '最后修改时间'
        super().__init__(*args, **kwargs)

class Modifier(models.ForeignKey):
    auto_field = True
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs['to'] = 'auth.User'
        kwargs['on_delete'] = models.SET_NULL
        kwargs['null'] = True
        kwargs['verbose_name'] = '修改人'
        super().__init__(*args, **kwargs)

