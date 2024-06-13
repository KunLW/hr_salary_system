from django import forms
from django.contrib import admin
from .models import Company, Department, Employee
from import_export.admin import ImportExportModelAdmin
from .resource import *
from django.utils.translation import gettext_lazy as _
from django.urls import re_path, reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
# Register your models here.
from rangefilter.filters import (
    DateRangeFilterBuilder,
    DateTimeRangeFilterBuilder,
    NumericRangeFilterBuilder,
    DateRangeQuickSelectListFilterBuilder,
)

from .action import *
'''
只导一次表: (employee) 新员工入职需要填写
基本薪资: 月薪调整系数, 餐补计划
社保公积金表(每年导入): 员工, 个人申报基数

每月导入表: (employee, effective_process)
考勤表 (从钉钉导入): 姓名, 工号, 出勤, 迟到, 早退, 上班缺卡, 下班缺卡, 旷工天数, 病假, 事假
	花名册中没有的人员跳过, 无数据的为零, 考勤表编号要人工添加
个税表 (从官网导入): 员工, 个税 
调整表 (月手工填报): 员工, 调整方向, 调整类型, 调整内容, 金额
'''
class DptChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "{} - {}".format(obj.company.short_name, obj.name)

Employee_exclude_fields = ['bank_name', 'bank_account_number', 'company', 'address', 'id_card_number']

export_selected_objects.short_description = "Export Selected"
export_selected_objects_xlsx.short_description = "Export Selected to XLSX"
create_salary_process.short_description = "创建薪酬单"



class EmployeeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    # add custom button
    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         re_path(r'^(?P<pk>[^/]+)/view/$', self.admin_site.admin_view(self.read_view), name='employee_view'),
    #     ]
    #     return custom_urls + urls

    # def read_view(self, request, pk):
    #     employee = get_object_or_404(Employee, pk=pk)
    #     context = dict(
    #         self.admin_site.each_context(request),
    #         title=employee.name,
    #         employee=employee,
    #     )
    #     return render(request, 'admin/employee_detail.html', context)
    
    # def view_details_button(self, obj):
    #     return format_html('<a class="button" href="{}">View Details</a>',
    #                        reverse('admin:employee_view', args=[obj.pk]))

    # view_details_button.short_description = 'View Details'
    # view_details_button.allow_tags = True

    # def has_view_permission(self, request, obj=None):
    #     return request.user.has_perm(f'{self.model._meta.app_label}.view_{self.model._meta.model_name}')

    #####
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'department':
            return DptChoiceField(queryset=Department.objects.all(), label='部门')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def company_dpt(self, obj):
        return obj.company.short_name + '-' + obj.department.name
    company_dpt.short_description = _('company department')
    company_dpt.admin_order_field = 'department__name'


    def pos_job(self, obj):
        return obj.position.name + ' ' + obj.job_position
    pos_job.short_description = _('position job')
    pos_job.admin_order_field = 'position__name'

    resource_class = EmployeeResource

    actions = [create_salary_process]
    list_display = ["employee_id", "name", "pos_job", 'company_dpt', "status", "employment_type" , "hire_date", "contract_end_date"]
    # list_editable = ["status",]
    date_hierarchy = 'hire_date'
    search_fields = ["employee_id", "name", "department", "company_dpt"]
    list_filter = ["company", "status", "employment_type", ('hire_date', DateRangeQuickSelectListFilterBuilder()),]
    # advanced_filter_fields = ['company', 'status', 'employment_type', 'department']

    fieldsets = (
        ('个人信息', {
            'fields': (
                ('employee_id', 'name'), 'id_card_number', ('gender', 'date_of_birth'), 
                'phone_number', ('native_city', 'address'), 'status'
            )
        }),
        ('工作信息', {
            'fields': (
                ('company', 'department'), ('position', 'job_position'), 
                ('hire_date', 'termination_date'), 'hr_document_number'
            )
        }),
        ('财务信息', {
            'fields': (
                'employment_type', ('bank_name', 'bank_account_number'),  
                ('contract_end_date', 'contract_term') , ('social_security_start_date', 
                'housing_fund_start_date'), 'record_in_jijian'
            )
        }),
        ('教育信息', {
            'fields': (
                ('major', 'graduate_school'), ('education_level', 'highest_degree')
            )
        }),
        ('其他信息', {
            'fields': (
                'in_labour_union_member', 'emergency_contact_phone', 
                'political_affiliation', 'notes'
            )
        }),
    )

    
    # row_id_fields = ('department',)
    # autocomplete_fields = ["department"]


class PromotionRecordInline(admin.TabularInline):
    model = PromotionRecord
    can_delete = False

    # extra = 3


class InternEmployeeAdmin(EmployeeAdmin):
    list_display = ["employee_id", "get_promotion_date", "name", "position", "job_position", 'company_dpt', "hire_date", "contract_end_date"]
    search_fields = ["employee_id", "name", "department", "company_dpt"]
    list_filter = ["company", "status",]
    inlines = [PromotionRecordInline]
    actions = [export_selected_objects, export_selected_objects_xlsx]

    def get_queryset(self, request):
        # 只显示status='A' 并且 employment_type = 'IN'的员工
        return super().get_queryset(request).filter(status='A', employment_type='IN')
    

    def get_promotion_date(self, obj):
        return PromotionRecord.objects.get(employee=obj).promotion_date
    get_promotion_date.short_description = '晋级日期'
    # get_promotion_date.admin_order_field = 'promotion_record__promotion_date'
    
class ActiveEmployeeAdmin(EmployeeAdmin):
    list_display = ["employee_id", "name", "position", "job_position", 'company_dpt', "employment_type", "hire_date", "contract_end_date"]
    search_fields = ["employee_id", "name", "department", "company_dpt"]
    list_filter = ["company", "status",]
    actions = [export_selected_objects, export_selected_objects_xlsx]

    def get_queryset(self, request):
        # 只显示status='A' 并且 employment_type = 'FT'的员工
        return super().get_queryset(request).filter(status='A')

class DimissionEmployeeAdmin(EmployeeAdmin):
    list_display = ["employee_id", "name", "position", "job_position", 'company_dpt', "employment_type", "hire_date", "contract_end_date"]
    search_fields = ["employee_id", "name", "company_dpt"]
    list_filter = ["company", "status",]
    readonly_fields = ['employee_id', 'id_card_number', 'department']
    actions = [export_selected_objects, export_selected_objects_xlsx]

    def get_queryset(self, request):
        # 只显示status='D'的员工
        return super().get_queryset(request).filter(status='D')
class CompanyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = CompanyResource
    list_display = ["company_id", "name", "short_name", "superior_company"]
    search_fields = ["company_id", "name"]
    list_filter = ["superior_company"]



class DepartmentFilter(admin.SimpleListFilter):
    title = 'department'
    parameter_name = 'department'

    def lookups(self, request, model_admin):
        departments = set([e.superior_department for e in model_admin.model.objects.all() if e.superior_department is not None])

        return [(d.department_id, d.name) for d in departments]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(department__department_id=self.value())
        return queryset
    

class DepartmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = DepartmentResource
    list_display = ["department_id", "name", "company", "superior_department"]
    search_fields = ["department_id", "name"]
    list_filter = ["company", DepartmentFilter]




admin.site.register(Company, CompanyAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
# admin.site.register(ActiveEmployee, ActiveEmployeeAdmin)
# admin.site.register(InternEmployee, InternEmployeeAdmin)
# admin.site.register(DimissionEmployee, DimissionEmployeeAdmin)


