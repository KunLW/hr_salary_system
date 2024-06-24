from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from employee.models import *
import logging
from . import rules
logger = logging.getLogger(__name__)


from django.db import models

class MonthlyAutoField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20  # 设置合适的长度
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add:
            now = timezone.now()
            year_month = now.strftime('%Y%m')
            last_instance = model_instance.__class__.objects.filter(
                auto_field__startswith=year_month).order_by('auto_field').last()
            
            if last_instance:
                last_id = int(last_instance.auto_field[len(year_month):])
                new_id = f"{year_month}{last_id + 1:04d}"
            else:
                new_id = f"{year_month}0001"

            setattr(model_instance, self.attname, new_id)
            return new_id
        else:
            return super().pre_save(model_instance, add)

# Position
class Position(models.Model):
    POSITION_TYPE = [
        ('m', _('Management Position')),
        ('p', _('Technocrat Position'))
    ]
    name = models.CharField(max_length=3, primary_key=True, verbose_name="岗级", unique=True)
    ensure_salary = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='基本工资')
    base_salary = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='月薪基数')
    type = models.CharField(choices=POSITION_TYPE, default='m', verbose_name='岗位类型')
    last_update = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("position")
        verbose_name_plural = _("positions")



# class InputPart(models.Model):
#     STATUS_CHOICES = [
#         ('N', _('No Entered')),
#         ('E', _('Entered')),
#         ('C', _('Checked')),
#         ('L', _('Locked')),
#     ]
#     salary_processes = models.ManyToManyField('SalaryProcess', verbose_name='工资条', blank=True)
#     name = models.CharField(max_length=50, verbose_name='名称', primary_key=True)
#     description = models.CharField(max_length=255, verbose_name='描述', blank=True)
#     input_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='录入人员', related_name='input_user', blank=True)
#     have_input = models.BooleanField(verbose_name='已录入', default=False)
#     check_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='审核人员', related_name='check_user', blank=True)
#     have_checked = models.BooleanField(verbose_name='已审核', default=False)
#     status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='状态', default='N')


class SalaryProcess(models.Model):
    STATUS_CHOICES = [
        ('E', _('Entering')),
        ('C', _('Checking')),
        ('P', _('Paying')),
        ('L', _('Locked')),
    ]
    id = models.AutoField(primary_key=True, verbose_name='编号', editable=False)
    month = models.CharField(max_length=7, verbose_name='生效月份')
    employees = models.ManyToManyField('employee.Employee', verbose_name='员工列表', blank=True)
    create_time = models.DateTimeField(verbose_name='生成时间', default=timezone.now, editable=False)
    last_update = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='状态', default='E')
    def __str__(self):
        return f"{self.id} 薪酬表"
    
    def calc(self):
        for employee in self.employees.all():
            # calculate salary and store them into SalaryDetail
            try:
                salary_detail = SalaryDetail.objects.get(employee=employee, effective_process=self)
                salary_detail.calc()
                salary_detail.save()
            except SalaryDetail.DoesNotExist:
                salary_detail = SalaryDetail.objects.create(employee=employee, effective_process=self)
                logger.info(f"生成工资明细记录{employee.employee_id} ")
                salary_detail.calc()
                salary_detail.save()
    class Meta:
        verbose_name = _('Salary Process')
        verbose_name_plural = _('Salary Process')


# Salary rules
class SalaryRule(models.Model):
    company = models.OneToOneField('employee.Company', on_delete=models.CASCADE, verbose_name='公司', primary_key=True)
    # basic salary rule

    # attendance rule
    super_meal_subsidy = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='驻场餐补')
    normal_meal_subsidy = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='普通餐补')

    # social security rule
    social_security_company_bear_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='公司承担社保基数', default=0.0)
    social_security_company_rate = models.DecimalField(max_digits=9, decimal_places=7, verbose_name='公司缴纳社保费率%')
    social_security_self_rate = models.DecimalField(max_digits=9, decimal_places=7, verbose_name='个人缴纳社保费率%')
    provident_fund_company_bear_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='公司承担公积金基数', default=0.0)
    provident_fund_company_rate = models.DecimalField(max_digits=9, decimal_places=7, verbose_name='公司缴纳公积金费率%')
    provident_fund_self_rate = models.DecimalField(max_digits=9, decimal_places=7, verbose_name='个人缴纳公积金费率%')
    
    # 工会费
    labor_union_fee_self_rate = models.DecimalField(max_digits=9, decimal_places=7, verbose_name='个人缴纳工会费率%', default=0.0)
    last_update = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)
    def __str__(self):
        return f"{self.company.name} 薪资规则"
    
    class Meta:
        verbose_name = _('Salary Rule')
        verbose_name_plural = _('Salary Rule')

# Standard Salary
class StdSalary(models.Model):
    # Keep in StdSalary
    MEAL_SUBSIDY_PLAN_CHOICES = [
        ('S', _('Super')),
        ('M', _('Normal')),
        ('N', _('None')),
    ]
    employee = models.OneToOneField('employee.Employee', on_delete=models.CASCADE, verbose_name='员工')
    base_salary_coefficient = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='月薪调整系数', default=1.00)
    meal_subsidy_plan = models.CharField(max_length=1, choices=MEAL_SUBSIDY_PLAN_CHOICES, default='M', verbose_name='餐补计划')
    last_update = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)
    #TODO: other salary that will be move to another Model
    # some employee information, employee id

    def __str__(self):
        return f"{self.employee.employee_id} {self.employee.name} 薪资标准"
    
    def clean(self) -> None:
        if self.base_salary_coefficient < 0:
            raise ValueError("Base salary coefficient must be greater than 0")

        return super().clean()

    class Meta:
        verbose_name = _('Standard Salary')
        verbose_name_plural = _('Standard Salary')



class Attendance(models.Model):
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE, verbose_name='员工', default=None)
    effective_process = models.ForeignKey('SalaryProcess', on_delete=models.CASCADE, verbose_name='生效薪酬表')
    total_work_days = models.IntegerField(verbose_name='全勤天数', null=True, blank=False)
    work_days = models.IntegerField(verbose_name='出勤天数', null=True, blank=False)
    # leave_days = models.IntegerField(verbose_name='非带薪请假天数', null=True, blank=False)

    late_times = models.IntegerField(verbose_name='迟到次数', null=True, blank=False)
    early_leave_times = models.IntegerField(verbose_name='早退次数', null=True, blank=False)
    punch_in_missing_times = models.IntegerField(verbose_name='上班缺卡次数', null=True, blank=False)
    punch_out_missing_times = models.IntegerField(verbose_name='下班缺卡次数', null=True, blank=False)
    absent_times = models.IntegerField(verbose_name='旷工天数', null=True, blank=False)
    no_salary_leave_duration = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='事假', null=True, blank=False)
    illness_leave_duration = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='病假', null=True, blank=False)
    last_update = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)
    def __str__(self):
        return f"{self.employee.employee_id} {self.employee.name} {self.effective_process.month} 考勤"
    
    class Meta:
        verbose_name = _('Attendance')
        verbose_name_plural = _('Attendance')
        unique_together = ['employee', 'effective_process']

# class Subsidy(models.Model):
#     MEAL_SUBSIDY_PLAN_CHOICES = [
#         ('S', _('Super')),
#         ('M', _('Normal')),
#         ('N', _('None')),
#     ]
#     employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE, verbose_name='员工')
#     effective_process = models.ForeignKey('SalaryProcess', on_delete=models.CASCADE, verbose_name='生效薪酬表')
#     meal_subsidy_plan = models.CharField(max_length=1, choices=MEAL_SUBSIDY_PLAN_CHOICES, default='M', verbose_name='餐补计划')
#     # weather_subsidy = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='防暑降温福利')
#     other_subsidy = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='其他福利')

#     def __str__(self):
#         return f"{self.employee.employee_id} {self.employee.name} {self.effective_process.month} 补贴"
    
#     class Meta:
#         verbose_name = _('Subsidy')
#         verbose_name_plural = _('Subsidy')
#         unique_together = ['employee', 'effective_process']
    
class SocialSecurityProvidentFund(models.Model):
    employee = models.OneToOneField('employee.Employee', on_delete=models.CASCADE, verbose_name='员工', unique=True)
    social_security_base_self_declare = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='个人申报社保基数', default=0.0)
    # social_security_amount_self_declare = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='个人承担社保金额', default=0.0)
    # social_security_amount_company_bear = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='公司承担社保金额', default=0.0)
    # social_security_additional_amount_self_bear = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='个人承担超额社保金额', default=0.0)

    provident_fund_base_self_declare = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='个人申报公积金基数', default=0.0)
    # provident_fund_amount_self_declare = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='个人承担公积金金额', default=0.0)
    # provident_fund_amount_company_bear = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='公司承担公积金金额', default=0.0)
    # provident_fund_additional_amount_self_bear = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='个人承担超额公积金金额', default=0.0)
    last_update = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)
    def __str__(self):
        return f"{self.employee.employee_id}{self.employee.name} 社保公积金"

    class Meta:
        verbose_name = _('Social Security Provident Fund')
        verbose_name_plural = _('Social Security Provident Fund')

class SalaryAdjustment(models.Model):
    ADJUSTMENT_TYPE_CHOICES = [
        ('I', _('Initial Salary')),
        ('S', _('Subsidy')),
        ('A', _('Assessment')),
        ('T', _('After Tax')),
    ]
    DIRECTION_CHOICES = [
        ('I', _('Increase')),
        ('D', _('Decrease')),
    ]
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE, verbose_name='员工')
    effective_process = models.ForeignKey('SalaryProcess', on_delete=models.CASCADE, verbose_name='生效薪酬表')
    direction = models.CharField(max_length=1, choices=DIRECTION_CHOICES, verbose_name='调整方向')
    adjustment_type = models.CharField(max_length=1, choices=ADJUSTMENT_TYPE_CHOICES, verbose_name='调整类型')
    description = models.CharField(max_length=255, verbose_name='调整内容')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额')
    notes = models.TextField(verbose_name='备注', blank=True)
    last_update = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)

    def __str__(self):
        return f"{self.employee.employee_id} {self.employee.name} {self.effective_process.month} 调整"

    class Meta:
        verbose_name = _('Salary Adjustment')
        verbose_name_plural = _('Salary Adjustments')
        unique_together = ['employee', 'effective_process', 'description']


from django.db import models

class TaxRecord(models.Model):
    ID_TYPE_CHOICES = [
        ('passport', _('Passport')),
        ('id_card', _('ID Card')),
        # 添加其他类型根据需要
    ]

    INCOME_ITEM_CHOICES = [
        ('salary', 'Salary'),
        ('bonus', 'Bonus'),
        # 添加其他所得项目根据需要
    ]

    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE, verbose_name="员工", null=True, blank=True)
    effective_process = models.ForeignKey('SalaryProcess', on_delete=models.CASCADE, verbose_name="薪酬表")
    income_item = models.CharField(max_length=50, verbose_name="所得项目")
    income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="本期收入")
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="税额")
    notes = models.TextField(blank=True, null=True, verbose_name="备注")

    def __str__(self):
        return f"{self.employee} - {self.effective_process} 税务"

    class Meta:
        verbose_name = "税务记录"
        verbose_name_plural = "税务记录"


class IncomeTax(models.Model):
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE, verbose_name='员工')
    effective_process = models.ForeignKey('SalaryProcess', on_delete=models.CASCADE, verbose_name='生效薪酬表')
    last_update = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)
    income_tax_base = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='个税起征点', null=True, blank=False)
    income_tax_rate = models.DecimalField(max_digits=9, decimal_places=7, verbose_name='个税税率', null=True, blank=False)
    income_tax_quick_deduction = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='个税速算扣除数', null=True, blank=False)
    income_tax = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='个税', null=True, blank=False)
    income_tax_deduction = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='个税扣款', null=True, blank=False)
    last_update = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)
    def __str__(self):
        return f"{self.employee.employee_id} {self.employee.name} {self.effective_process.month} 个税"
    
    class Meta:
        verbose_name = _('Income Tax')
        verbose_name_plural = _('Income Tax')
        unique_together = ['employee', 'effective_process']


class SalaryDetail(models.Model):
    # Basic Information
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE, verbose_name='员工')
    effective_process = models.ForeignKey('SalaryProcess', on_delete=models.CASCADE, verbose_name='生效薪酬表')
    last_update = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)
    base_salary_coefficient = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='月薪调整系数', null=True, blank=False)
    base_salary = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='月薪基数', null=True, blank=False)
    std_salary = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='定岗满勤标准月薪', null=True, blank=False) # from rules.py
    std_ensured_salary = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='定岗月基本工资', null=True, blank=False) # from position
    std_merit_salary = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='定岗月基本绩效工资', null=True, blank=False) # from assessment
    no_salary_leave_deduction = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='非带薪请假扣款', null=True, blank=False) # from rules.py
    
    # other_salary_deduction = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='其他薪资调整减少项', null=True, blank=False) 
    salary_increase = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='调整增加项', null=True, blank=False)
    salary_decrease = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='调整减少项', null=True, blank=False) # 只放极简信息
    total_salary = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='当月月薪合计', null=True, blank=False)

    # 福利
    meal_subsidy = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='餐补', null=True, blank=False) # from rules.py
    # weather_subsidy = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='防暑降温福利', null=True, blank=False) # 只放极简
    # rental_subsidy = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='租房补贴', null=True, blank=False) # 只对上
    other_subsidy = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='其他福利', null=True, blank=False)
    total_subsidy = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='当月福利合计', null=True, blank=False)

    salary_before_assessment = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='考核前当月薪酬', null=True, blank=False)

    # 考核
    attendance_deduction = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='考勤考核绩效扣款', null=True, blank=False) # 导入
    # other_assessment_deduction = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='其他考核绩效扣款', null=True, blank=False)
    assessment_increase = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='考核绩效增加项', null=True, blank=False)
    assessment_decrease = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='考核绩效减少项', null=True, blank=False)

    # 当月应发薪酬
    total_salary_before_tax_and_fee = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='当月应发薪酬', null=True, blank=False)

    # 社保公积金
    social_security_provident_fund_self_bear = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='个人承担超额缴纳部分', null=True, blank=False)

    #
    total_salary_for_tax_calc = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='当月计税薪酬', null=True, blank=False)

    fee_self_bear = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='代扣代缴费用', null=True, blank=False)

    tax_self_bear = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='代扣个税', null=True, blank=False)

    # 当月税后薪酬
    total_salary_after_tax = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='当月税后薪酬', null=True, blank=False)

    increase_after_tax = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='税后增加项', null=True, blank=False)

    decrease_after_tax = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='税后减少项', null=True, blank=False)

    
    def __str__(self):
        return f"{self.employee.employee_id} {self.employee.name} {self.effective_process.month} 工资条"
    
    def calc(self):
        exclude_fields = {'id', 'employee', 'effective_process', 'last_update'}
        print(f"计算 {self.employee} {self.effective_process}")
        field_list = [field for field in self._meta.get_fields() if field.name not in exclude_fields]
        print(f"计算 {field_list}")
        for field in field_list:
            field_name = field.name
            verbose_name = field.verbose_name
            print(f"计算 {verbose_name}")
            func_name = f'calc_{field_name}'
            if hasattr(rules, func_name):
                try:
                    setattr(self, field_name, getattr(rules, func_name)(self.employee, self.effective_process))
                except Exception:
                    raise AttributeError(f"{verbose_name}计算错误")
            else:
                raise AttributeError(f"Missing calculation rule for {field_name}")

    class Meta:
        verbose_name = _('Salary Detail')
        verbose_name_plural = _('Salary Detail')
        unique_together = ['employee', 'effective_process']



