from django.http import HttpResponse
from import_export.admin import ExportMixin

from employee.models import *

from django.contrib import messages

from django.db.models.query import QuerySet

def calc_salary_detail(modeladmin, request, queryset):
    print(f"开始计算工资明细{queryset.all()}")
    for salary_process in queryset:
        print(f"开始计算工资明细{salary_process}")
        try:
            salary_process.calc()
            messages.add_message(request, messages.INFO, f"计算工资明细{salary_process}成功")
        except Exception as e:
            messages.add_message(request, messages.ERROR, f"计算工资明细失败，错误信息：{e}")
        