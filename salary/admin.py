from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from .forms import *
from .resources import *
# Register your models here.

from . import actions


class PositionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PositionResource
    list_display = ['name', 'last_update', 'ensure_salary', 'base_salary', 'type']
    list_filter = ['type']

class SalaryRuleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['company', 'last_update', 'super_meal_subsidy', 'normal_meal_subsidy', 'social_security_company_bear_base', 'social_security_company_rate', 'social_security_self_rate', 'provident_fund_company_bear_base', 'provident_fund_company_rate', 'provident_fund_self_rate', 'labor_union_fee_self_rate']
    fieldsets = [
        (None, {'fields': ['company']}),
        ('餐补福利规则', {'fields': ['super_meal_subsidy', 'normal_meal_subsidy']}),
        ('社保公积金工会规则', {'fields': [('social_security_company_bear_base', 'social_security_company_rate', 'social_security_self_rate'), ('provident_fund_company_bear_base', 'provident_fund_company_rate', 'provident_fund_self_rate'), 'labor_union_fee_self_rate']}),
    ]



class StdSalaryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = StdSalaryResource
    list_display = ['employee', 'last_update', 'base_salary', 'base_salary_coefficient', 'meal_subsidy_plan']
    def base_salary(self, obj):
        return obj.employee.position.base_salary
    base_salary.short_description = '基本工资'
    base_salary.admin_order_field = 'employee__position__base_salary'
    # readonly_fields = ['employee', 'base_salary', ]
#     list_filter = ['employee']

class SocialSecurityProvidentFundAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = SocialSecurityProvidentFundResource
    list_display = ['employee', 'last_update', 'social_security_base_self_declare', 'provident_fund_base_self_declare', ]
    # readonly_fields = ['employee',
    #                    'social_security_amount_self_declare', 
    #                    'social_security_amount_company_bear', 
    #                    'social_security_additional_amount_self_bear',
    #                    'provident_fund_amount_self_declare',
    #                    'provident_fund_amount_company_bear',
    #                    'provident_fund_additional_amount_self_bear']
    list_filter = ['employee__company']
    # fieldsets = [
    #     (None, {'fields': [('employee')]}),
    #     ('社保公积金基数', {'fields': [('social_security_base_self_declare', 'provident_fund_base_self_declare')]}),
    #     ('社保金额', {'fields': [('social_security_amount_self_declare', 'social_security_amount_company_bear'), 'social_security_additional_amount_self_bear']}),
    #     ('公积金金额', {'fields': [('provident_fund_amount_self_declare', 'provident_fund_amount_company_bear'), 'provident_fund_additional_amount_self_bear']}),
    # ]

actions.calc_salary_detail.short_description = '计算工资明细'
class AttendanceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AttendanceResource
    all_fields = [f for f in Attendance._meta.get_fields() if f.name != 'id']
    list_display = [f.name for f in all_fields]
    readonly_fields = [f.name for f in all_fields]
    list_filter = ['employee__company', 'effective_process__month']
    

class SalaryProcessAdmin(admin.ModelAdmin):
    def employees_count(self, obj: SalaryProcess):
        return obj.employees.count()
    actions = [actions.calc_salary_detail]
    employees_count.short_description = '员工数'
    list_display = ['id', 'month', 'status', 'create_time', 'last_update', 'employees_count']

class SalaryDetailAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = SalaryDetailResource
    # list_display = ['employee', 'effective_process', 'total_salary', 'total_subsidy', 'salary_before_assessment', 'assessment_decrease', 'total_salary_before_tax_and_fee', 'fee_self_bear', 'total_salary_for_tax_calc', 'total_salary_after_tax']
    all_fields = [f for f in SalaryDetail._meta.get_fields() if f.name != 'id']
    list_display = [f.name for f in all_fields]
    readonly_fields = [f.name for f in all_fields]
    list_filter = ['employee__company', 'effective_process__month']

class SalaryAdjustmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = SalaryAdjustmentResource
    list_display = ['employee', 'effective_process', 'direction', 'adjustment_type', 'description', 'amount',  'last_update']
    list_filter = ['direction', 'adjustment_type']
    fieldsets = [
        (None, {'fields': ['employee', 'effective_process']}),
        ('调整内容', {'fields': ['direction', 'adjustment_type', 'description', 'amount']}),
    ]

class IncomeTaxAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = IncomeTaxResource
    all_fields = [f for f in IncomeTax._meta.get_fields() if f.name != 'id']
    list_display = [f.name for f in all_fields]
    readonly_fields = [f.name for f in all_fields]
    list_filter = ['employee__company', 'effective_process__month']

class TaxRecordAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = TaxRecordResource
    all_fields = [f for f in TaxRecord._meta.get_fields()]
    list_display = [f.name for f in all_fields]
    # readonly_fields = [f.name for f in all_fields]
    list_filter = ['effective_process__month']

admin.site.register(Position, PositionAdmin)
admin.site.register(SalaryRule, SalaryRuleAdmin)
admin.site.register(SalaryProcess, SalaryProcessAdmin)
admin.site.register(SalaryDetail, SalaryDetailAdmin)
admin.site.register(StdSalary, StdSalaryAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(TaxRecord, TaxRecordAdmin)
admin.site.register(SocialSecurityProvidentFund, SocialSecurityProvidentFundAdmin)
admin.site.register(SalaryAdjustment, SalaryAdjustmentAdmin)
# admin.site.register(IncomeTax, IncomeTaxAdmin)