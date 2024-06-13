from typing import Any
from django.db import models

# Create your models here.
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from salary.models import Position
from django.urls import reverse
from django.utils.html import format_html
# Create your models here.
class Company(models.Model):
    # Basic Information
    company_id = models.CharField(max_length=7, primary_key=True, verbose_name="编号", unique=True)
    name = models.CharField(max_length=100, verbose_name="公司名称", unique=True)
    short_name = models.CharField(max_length=50, verbose_name="公司简称", unique=True)
    superior_company = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="上级公司")
    
    def custom_button(self, obj):
        url = reverse('admin:custom_view', args=[obj.id])
        return format_html('<a class="button" href="{}">Custom Button</a>', url)    
        

    def __str__(self):
        return self.name
    
    def clean(self):
        # 检查公司名称和简称是否匹配
        # if self.short_name not in self.name:
        #     raise ValidationError("公司名称和简称不匹配")
        pass
    class Meta:
        verbose_name = _("company")
        verbose_name_plural = _("companies")
        ordering = ["company_id"]

class Department(models.Model):
    # Basic Information
    department_id = models.CharField(max_length=10, primary_key=True, verbose_name="编号")
    name = models.CharField(max_length=100, verbose_name="部门名称")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="所属公司")
    superior_department = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="上级部门")
    # date_ranges = models.JSONField(default=list,null=True, blank=True, )
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("department")
        verbose_name_plural = _("departments")
        ordering = ["department_id"]



class Employee(models.Model):
    STATUS_CHOICES = [
        ('A', _('Active')),
        ('D', _('Dimission')),
        ('R', _('Retired')),
    ]
    BANK_CHOICES = [
            ('BPI', _('Bank of the Philippine Islands')),
            ('BDO', _('Banco de Oro')),
            ('METRO', _('Metrobank')),
            ('PNB', _('Philippine National Bank')),
            ('LANDBANK', _('Land Bank of the Philippines')),
            ('UCPB', _('United Coconut Planters Bank')),
            ('DBP', _('Development Bank of the Philippines')),
            ('RCBC', _('Rizal Commercial Banking Corporation')),
            ('SECURITY', _('Security Bank')),
            ('EASTWEST', _('EastWest Bank')),
            ('CHINA', _('China Bank')),
            ('HSBC', _('HSBC')),
            ('CITI', _('Citibank')),
            ('PNB', _('Philippine National Bank')),
            ('OTHERS', _('Others')),
            ('CZB', _('China Zheshang Bank')),

    ]
    EMPLOYEE_TYPE = [# 全日制, 实习生, 试用期, 退休返聘, 合伙人
        ('FT', _('Full-time')),
        ('IN', _('Intern')),
        ('PB', _('Probation')),
        ('RH', _('Re-hire')),
        ('CP', _('Cooperator')),
    ]
    GENDER_CHOICES = [('M', _('male')), ('F', _('female'))]


    # 个人信息
    employee_id = models.CharField(primary_key=True, max_length=20, unique=True, verbose_name="编号")
    name = models.CharField(max_length=100, verbose_name="姓名", null=True, blank=True)
    id_card_number = models.CharField(max_length=22, unique=True, verbose_name="身份证号码", null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="性别", null=True, blank=True)
    phone_number = models.CharField(max_length=70, verbose_name="联系电话", null=True, blank=True)
    native_city = models.CharField(max_length=50, verbose_name="籍贯", null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name="联系地址", null=True, blank=True)
    date_of_birth = models.DateField(verbose_name="出生年月", null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="员工状态", default='A')

    # 工作信息
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="公司", null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="部门", null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="岗级", null=True, blank=True)
    job_position = models.CharField(max_length=100, verbose_name="岗位", null=True, blank=True, default="无岗")
    hire_date = models.DateField(verbose_name="入职时间", null=True, blank=True)
    termination_date = models.DateField(verbose_name="离职时间", null=True, blank=True)
    hr_document_number = models.CharField(max_length=100, verbose_name="人事资料编号", null=True, blank=True)

    # 财务信息
    # insured_company = models.CharField(max_length=100, verbose_name="参保公司", null=True, blank=True)
    # online_department = models.CharField(max_length=100, verbose_name="线上部门", null=True, blank=True)
    bank_name = models.CharField(max_length=100, choices=BANK_CHOICES, verbose_name="开户行", null=True, blank=True)
    bank_account_number = models.CharField(max_length=50, verbose_name="开户行账号", null=True, blank=True)
    employment_type = models.CharField(max_length=50, verbose_name="用工形式", choices=EMPLOYEE_TYPE, default='FT')
    contract_term = models.DurationField(verbose_name="合同期限", null=True, blank=True)
    contract_end_date = models.DateField(verbose_name="劳动合同到期时间", null=True, blank=True)
    social_security_start_date = models.DateField(verbose_name="社保始缴日", null=True, blank=True)
    housing_fund_start_date = models.DateField(verbose_name="公积金始缴日", null=True, blank=True)
    record_in_jijian = models.BooleanField(verbose_name="是否通过极简", default=True)

    # 教育信息
    major = models.CharField(max_length=100, verbose_name="毕业专业", null=True, blank=True)
    graduate_school = models.CharField(max_length=100, verbose_name="毕业学校", null=True, blank=True)
    education_level = models.CharField(max_length=50, verbose_name="文化程度", null=True, blank=True)
    highest_degree = models.CharField(max_length=50, verbose_name="最高学历", null=True, blank=True)

    # 其他信息
    in_labour_union_member = models.BooleanField(verbose_name="是否为工会会员", default=True)
    emergency_contact_phone = models.CharField(max_length=15, verbose_name="紧急联系电话", null=True, blank=True)
    political_affiliation = models.CharField(max_length=50, verbose_name="政治面貌", null=True, blank=True)
    notes = models.TextField(blank=True, verbose_name="备注", null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="最后修改时间")

    def __str__(self):
        return self.name
    
        
    def clean(self):
        # 检查公司名称和简称是否匹配
        if self.department.company.name != self.company.name:
            raise ValidationError("公司和部门不匹配")

    class Meta:
        verbose_name = _("employee")
        verbose_name_plural = _("employees")
        

class PromotionRecord(models.Model):
    employee = models.OneToOneField('Employee', on_delete=models.CASCADE, verbose_name="员工")
    promotion_date = models.DateField(verbose_name="晋升日期")

    def __str__(self):
        return f"{self.employee.name} - {self.promotion_date}"
    
    def delete(self, using: Any = ..., keep_parents: bool = ...) -> tuple[int, dict[str, int]]:
        return super().delete(using, keep_parents)
    class Meta:
        verbose_name = _("promotion record")
        verbose_name_plural = _("promotion records")

class InternEmployee(Employee):
    
    class Meta:
        proxy = True
        verbose_name = _('Intern Employee')
        verbose_name_plural = _('Intern Employees')


class ActiveEmployee(Employee):
    class Meta:
        proxy = True
        verbose_name = _('Active Employee')
        verbose_name_plural = _('Active Employees')

class DimissionEmployee(Employee):
    class Meta:
        proxy = True
        verbose_name = _('Dimission Employee')
        verbose_name_plural = _('Dimission Employees')