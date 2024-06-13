from django.http import HttpResponse
from import_export.admin import ExportMixin
from .models import *
from .resource import *
from salary.models import *
from django.utils import timezone
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)
def export_selected_objects(modeladmin, request, queryset):
    resource = EmployeeActionResource()
    dataset = resource.export(queryset)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=export.csv'
    return response

def export_selected_objects_xlsx(modeladmin, request, queryset):
    resource = EmployeeActionResource()
    dataset = resource.export(queryset)
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=export.xlsx'
    return response

def create_salary_process(modeladmin, request, queryset):
    try:
        salary_process = SalaryProcess.objects.create()
        salary_process.month = timezone.now().strftime('%Y-%m')
        salary_process.employees.set(queryset)
        employee_count = salary_process.employees.count()
        salary_process.save()
        print('====salary process created====')
        init_all_tables(salary_process)
    except Exception as e:
        logger.error(f"创建工资流程失败，错误信息：{e}")
        messages.add_message(request, messages.ERROR, f"创建工资流程失败，错误信息：{e}")
        return
    messages.add_message(request, messages.INFO, f"创建工资流程成功，员工数：{employee_count}")




def init_all_tables(instance):
    try:
        employees = instance.employees.all()
        print(f"====salaryProcess {employees}====")
        for employee in employees:
            # create std salary for each employee
            std_salary, std_salary_created = StdSalary.objects.get_or_create(employee=employee)
            if std_salary_created:
                std_salary.save()
                logger.info(f"生成基础薪资记录{employee.employee_id} ")
            # create salary detail for each employee
            salary_detail = SalaryDetail.objects.create(employee=employee, effective_process=instance)
            salary_detail.save()
            # create social security provident fund for each employee
            sspf, sspf_created = SocialSecurityProvidentFund.objects.get_or_create(employee=employee)
            if sspf_created:
                sspf.save()
                logger.info(f"生成社保公积金记录{employee.employee_id} ")
            # create attendance for each employee
            attendance = Attendance.objects.create(employee=employee, effective_process=instance)
            attendance.save()

    except Exception as e:
        raise e
