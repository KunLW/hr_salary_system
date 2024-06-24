from .genericResource import *

from import_export.widgets import Widget
import json
from datetime import datetime
from .models import *
from employee.models import Employee

class PositionResource(GenericModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(model=Position, *args, **kwargs)

    class Meta:
        model = Position
        import_id_fields = ['name']
        skip_unchanged = True

class SalaryAdjustmentResource(GenericModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(model=SalaryAdjustment, *args, **kwargs)

    class Meta:
        model = SalaryAdjustment
        import_id_fields = ['employee', 'effective_process']
        skip_unchanged = True
        exclude = ('id', 'last_update')


class SalaryDetailResource(GenericModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(model=SalaryDetail, *args, **kwargs)

    class Meta:
        model = SalaryDetail
        import_id_fields = ['employee', 'salary_process']
        skip_unchanged = True

class IncomeTaxResource(GenericModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(model=IncomeTax, *args, **kwargs)

    class Meta:
        model = IncomeTax
        import_id_fields = ['employee', 'effective_process']
        skip_unchanged = True
        exclude = ('id', 'last_update')

class RosterWidget(ForeignKeyWidget):
    def get_queryset(self, value, row, *args, **kwargs):
        return self.model.objects.filter(id_card_number=value)

    def clean(self, value, row=None, *args, **kwargs):
        return self.get_queryset(value, row, *args, **kwargs).get()
from import_export.widgets import ForeignKeyWidget
class TaxRecordResource(resources.ModelResource):
    id_num = fields.Field(column_name='身份证号码', widget=ForeignKeyWidget(Employee, 'id_card_number'))
    effec_process = fields.Field(column_name='生效薪资单', attribute='effective_process')
    income_item = fields.Field(column_name='所得项目', attribute='income_item' )
    income = fields.Field(column_name='本期收入', attribute='income')
    tax_amount = fields.Field(column_name='应补(退)税额', attribute='tax_amount')
    

    def before_import_row(self, row, **kwargs):
        try: 
            row['employee'] = Employee.objects.get(id_card_number=row['id_num'])
        except Employee.DoesNotExist:
            raise Exception(f"员工{row['id_num']}不存在")
        except Employee.MultipleObjectsReturned:
            raise Exception(f"员工{row['id_num']}不唯一")
        del row['id_num']


    class Meta:
        model = TaxRecord
        import_id_fields = ['id_num', 'effective_process']
        skip_unchanged = True
        exclude = ('id', 'employee', 'effective_process', 'notes')
class AttendanceResource(GenericModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(model=Attendance, *args, **kwargs)

    class Meta:
        model = Attendance
        import_id_fields = ['employee', 'effective_process']
        skip_unchanged = True
        exclude = ('id', 'last_update')

class SocialSecurityProvidentFundResource(GenericModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(model=SocialSecurityProvidentFund, *args, **kwargs)

    class Meta:
        model = SocialSecurityProvidentFund
        import_id_fields = ['employee']
        skip_unchanged = True
        exclude = ('id', 'last_update')
class StdSalaryResource(GenericModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(model=StdSalary, *args, **kwargs)

    class Meta:
        model = StdSalary
        import_id_fields = ['employee']
        skip_unchanged = True
        exclude = ('id', 'last_update')

