from import_export import resources, fields, widgets
from datetime import datetime
from myfields import MonthField

class ForeignKeyWidgetByName(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        try:
            return self.model.objects.get(name=value)
        except self.model.DoesNotExist:
            print(f"{self.model.__name__} matching query does not exist: {value}")
            return None
        
    def render(self, value, obj=None):
        if value is None:
            return ""
        return getattr(value, self.field, None)

class ChoiceDisplayWidget(widgets.Widget):
    '''
    A widget that converts between the display value of a choice field and its actual
    '''
    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = choices

    def clean(self, value, row=None, *args, **kwargs):
        '''
        Convert the display value to the actual value
        '''
        for choice_value, choice_display in self.choices:
            if choice_display == value:
                return choice_value
        return None

    def render(self, value, obj=None):
        '''
        Convert the actual value to the display value
        '''
        for choice_value, choice_display in self.choices:
            if value == choice_value:
                return choice_display
        return None

from import_export.widgets import Widget
import datetime

class MonthWidget(Widget):
    def clean(self, value, row=None, *args, **kwargs):
        # 从导入的数据中读取并转换日期
        return datetime.datetime.strptime(value, '%Y-%m').date()

    def render(self, value, obj=None):
        # 将日期转换为导出的格式
        if value:
            return value.strftime('%Y-%m')
        return ""

from import_export.widgets import ForeignKeyWidget

from django.db import models
from django.utils.encoding import force_str

# class SlashWrapperWidget(Widget):
#     def __init__(self, original_widget):
#         self.original_widget = original_widget

#     def render(self, value, obj=None):
#         original_value = self.original_widget.render(value, obj)
#         return original_value if original_value else '/'

#     def clean(self, value, row=None, *args, **kwargs):
#         if value == '/':
#             return ''
#         return self.original_widget.clean(value, row, *args, **kwargs)


# class GenericModelResource(resources.ModelResource):
#     def __init__(self, model, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.get_fields():
#             field_name = self.get_field_name(field)
#             verbose_name = model._meta.get_field(field_name).verbose_name
            
#             model_field = model._meta.get_field(field_name)
#             # print(field)
            
#             if isinstance(field, fields.Field):
#                 if isinstance(field, MonthField):
#                     # print("=====Find MonthField=====")
#                     original_widget = MonthDisplayWidget()
#                 elif isinstance(model_field, models.ForeignKey):
#                     # print("=====Find ForeignKey=====")
#                     original_widget = field.widget
#                     # original_widget = ForeignKeyWidget(model_field.related_model, 'name')
#                     # original_widget = ForeignKeyRawIdWidget(model_field.remote_field, self.admin_site)
#                 elif model_field.choices:
#                     original_widget = ChoiceDisplayWidget(model_field.choices)
#                 else:
#                     original_widget = field.widget
#             else:
#                 original_widget = widgets.Widget()
            
#             self.fields[field_name] = fields.Field(attribute=field_name, 
#                                                    column_name=force_str(verbose_name), 
#                                                    widget=original_widget)
        
    
#     # def get_field_name(self, field):
#     #     return field.attribute or field.column_name

#     # def get_fields(self):
#     #     return self.fields.values()
    
#     def skip_row(self, instance, original, row, import_validation_errors=None):
#         if all(value in [None, ""] for value in row.values()):
#             print("an empty input found")
#             return True
#         return super().skip_row(instance, original, row, import_validation_errors=import_validation_errors)

from import_export import fields, widgets
from django.utils.encoding import force_str

class MixinModelResource(resources.ModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        mixin_exclude_fields = ['create_time', 'last_modified', 'modifier']
        mixin_exclude_fields.extend(getattr(self.Meta, 'exclude_fields', []))
        self.fields = {k: v for k, v in self.fields.items() if k not in mixin_exclude_fields}
        for field_name, field in self.fields.items():
            # print(field_name)
            model_field = self.Meta.model._meta.get_field(field_name)
            verbose_name = model_field.verbose_name
            original_widget = None
            # 检查ForeignKey和choices属性，保留原有逻辑
                
            if model_field.choices:
                original_widget = ChoiceDisplayWidget(model_field.choices)
            # 检查MonthField并应用MonthWidget
            elif isinstance(model_field, MonthField):  # 假设MonthField是自定义字段类型
                original_widget = MonthWidget()
            # 如果没有匹配的widget，则使用原始widget
            # print("original_widget: ", original_widget)
            if original_widget is None:
                # print("No widget found for field: ", field_name, "using default widget", field.widget)
                self.fields[field_name] = fields.Field(attribute=field_name, 
                                                   column_name=force_str(verbose_name),
                                                   widget=field.widget)
            else:
                self.fields[field_name] = fields.Field(attribute=field_name, 
                                                   column_name=force_str(verbose_name), 
                                                   widget=original_widget)
                
        
        

class ReadableModelResource(resources.ModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            print(field_name)
            model_field = self.Meta.model._meta.get_field(field_name)
            verbose_name = model_field.verbose_name
            original_widget = None
            # 检查ForeignKey和choices属性，保留原有逻辑
            if hasattr(model_field, 'related_model') and model_field.related_model is not None:
                original_widget = ForeignKeyWidget(model_field.related_model, 'name')
            elif model_field.choices:
                original_widget = ChoiceDisplayWidget(model_field.choices)
            # 检查MonthField并应用MonthWidget
            elif isinstance(model_field, MonthField):  # 假设MonthField是自定义字段类型
                original_widget = MonthWidget()
            # 如果没有匹配的widget，则使用原始widget
            print("original_widget: ", original_widget)
            if original_widget is None:
                print("No widget found for field: ", field_name, "using default widget", field.widget)
                self.fields[field_name] = fields.Field(attribute=field_name, 
                                                   column_name=force_str(verbose_name),
                                                   widget=field.widget)
            else:
                self.fields[field_name] = fields.Field(attribute=field_name, 
                                                   column_name=force_str(verbose_name), 
                                                   widget=original_widget)


class GenericModelActionResource(resources.ModelResource):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.get_fields():
            field_name = self.get_field_name(field)
            verbose_name = model._meta.get_field(field_name).verbose_name
            
            model_field = model._meta.get_field(field_name)
            
            if isinstance(field, fields.Field):
                if isinstance(model_field, models.ForeignKey):
                    original_widget = ForeignKeyWidget(model_field.related_model, 'name')
                    # original_widget = field.widget
                elif model_field.choices:
                    original_widget = ChoiceDisplayWidget(model_field.choices)
                else:
                    original_widget = field.widget
            else:
                original_widget = widgets.Widget()
            
            self.fields[field_name] = fields.Field(attribute=field_name, 
                                                   column_name=force_str(verbose_name), 
                                                   widget=original_widget)
    
    # def get_field_name(self, field):
    #     return field.attribute or field.column_name

    # def get_fields(self):
    #     return self.fields.values()
    
    def skip_row(self, instance, original, row, import_validation_errors=None):
        if all(value in [None, ""] for value in row.values()):
            print("an empty input found")
            return True
        return super().skip_row(instance, original, row, import_validation_errors=import_validation_errors)
    
