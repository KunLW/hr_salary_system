from .genericResource import *
from import_export.widgets import Widget
import json
from datetime import datetime
from .models import Company
class CompanyResource(GenericModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(model=Company, *args, **kwargs)

    class Meta:
        model=Company
        import_id_fields = ['company_id']
        skip_unchanged = True


class DateRangeListWidget(Widget):
    def clean(self, value, row=None, *args, **kwargs):
        try:
            date_ranges = json.loads(value)
            # Ensure each item in the list is a tuple of valid dates
            cleaned_date_ranges = [
                (datetime.strptime(start, '%Y-%m-%d'), datetime.strptime(end, '%Y-%m-%d'))
                for start, end in date_ranges
            ]
            return cleaned_date_ranges
        except (ValueError, TypeError):
            return []

    def render(self, value, obj=None):
        if value:
            return json.dumps([
                (start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
                for start, end in value
            ])
        return json.dumps([])
    
    
from .models import Department
class DepartmentResource(GenericModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(model=Department, *args, **kwargs)
        


    
    class Meta:
        model = Department
        import_id_fields = ['department_id']

        skip_unchanged = True

from .models import Employee
from import_export.fields import Field
from import_export import resources
class EmployeeResource(GenericModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(model=Employee, *args, **kwargs)

    class Meta:
        model = Employee
        import_id_fields = ['employee_id']
        skip_unchanged = True

class EmployeeActionResource(GenericModelActionResource):
    def __init__(self, *args, **kwargs):
        super().__init__(model=Employee, *args, **kwargs)
        self.fields['dpt_id'] = Field(column_name='部门 ID', 
                        attribute='department',
                        widget=ForeignKeyWidget(Department, 'department_id')
                              )
    
    class Meta:
        model = Employee
        import_id_fields = ['employee_id']
        # fields = ['employee_id', 'name', 'department', 'dpt_id']
        skip_unchanged = True