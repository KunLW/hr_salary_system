from .genericResource import *

from import_export.widgets import Widget
import json
from datetime import datetime
from .models import *

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


class AttendanceResource(GenericModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(model=Attendance, *args, **kwargs)

    class Meta:
        model = Attendance
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