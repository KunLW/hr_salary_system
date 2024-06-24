from django import forms
from django.core.exceptions import ValidationError
import datetime
class CustomMonthField(forms.CharField):
    def __init__(self, **kwargs):
        # 初始化时，设置默认的widget为TextInput，并设置placeholder属性
        kwargs['widget'] = forms.TextInput(attrs={'placeholder': 'YYYY-MM', type: 'month'})
        super().__init__(**kwargs)

    def to_python(self, value):
        if value is None or value == '':
            return None
        try:
            return datetime.datetime.strptime(value, '%Y-%m')
        except ValueError:
            raise ValidationError('Invalid date format, please use YYYY-MM')
        
    def prepare_value(self, value):
        if value is None or value == '':
            return None
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m')
        return value
    
    # def widget_attrs(self, widget):
    #     attrs = super().widget_attrs(widget)
    #     attrs['type'] = 'month'
    #     return attrs
    
    def validate(self, value):
        super().validate(value)
        if value is None or value == '':
            return
        if not isinstance(value, datetime.datetime):
            raise ValidationError('错误的日期格式，请使用YYYY-MM')

