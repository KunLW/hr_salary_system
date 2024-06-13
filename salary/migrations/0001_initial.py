# Generated by Django 5.0.6 on 2024-06-12 05:27

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('name', models.CharField(max_length=3, primary_key=True, serialize=False, unique=True, verbose_name='岗级')),
                ('ensure_salary', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='基本工资')),
                ('base_salary', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='月薪基数')),
                ('type', models.CharField(choices=[('m', 'Management Position'), ('p', 'Technocrat Position')], default='m', verbose_name='岗位类型')),
            ],
            options={
                'verbose_name': 'position',
                'verbose_name_plural': 'position',
            },
        ),
        migrations.CreateModel(
            name='SalaryRule',
            fields=[
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='employee.company', verbose_name='公司')),
                ('super_meal_subsidy', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='驻场餐补')),
                ('normal_meal_subsidy', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='普通餐补')),
                ('social_security_company_bear_base', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='公司承担社保基数')),
                ('social_security_company_rate', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='公司缴纳社保费率%')),
                ('social_security_self_rate', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='个人缴纳社保费率%')),
                ('provident_fund_company_bear_base', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='公司承担公积金基数')),
                ('provident_fund_company_rate', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='公司缴纳公积金费率%')),
                ('provident_fund_self_rate', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='个人缴纳公积金费率%')),
                ('labor_union_fee_self_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='个人缴纳工会费率%')),
            ],
            options={
                'verbose_name': 'Salary Rule',
                'verbose_name_plural': 'Salary Rule',
            },
        ),
        migrations.CreateModel(
            name='SalaryProcess',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='生成时间')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
                ('month', models.CharField(blank=True, max_length=7, verbose_name='生效月份')),
                ('status', models.CharField(choices=[('E', 'Entering'), ('C', 'Checking'), ('P', 'Paying'), ('L', 'Locked')], default='E', max_length=1, verbose_name='状态')),
                ('employees', models.ManyToManyField(blank=True, to='employee.employee', verbose_name='员工列表')),
            ],
            options={
                'verbose_name': 'Salary Process',
                'verbose_name_plural': 'Salary Process',
            },
        ),
        migrations.CreateModel(
            name='InputPart',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='名称')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='描述')),
                ('have_input', models.BooleanField(default=False, verbose_name='已录入')),
                ('have_checked', models.BooleanField(default=False, verbose_name='已审核')),
                ('status', models.CharField(choices=[('N', 'No Entered'), ('E', 'Entered'), ('C', 'Checked'), ('L', 'Locked')], default='N', max_length=1, verbose_name='状态')),
                ('check_user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='check_user', to=settings.AUTH_USER_MODEL, verbose_name='审核人员')),
                ('input_user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='input_user', to=settings.AUTH_USER_MODEL, verbose_name='录入人员')),
                ('salary_processes', models.ManyToManyField(blank=True, to='salary.salaryprocess', verbose_name='工资条')),
            ],
        ),
        migrations.CreateModel(
            name='StdSalary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_salary_coefficient', models.DecimalField(decimal_places=2, default=1.0, max_digits=5, verbose_name='月薪调整系数')),
                ('meal_subsidy_plan', models.CharField(choices=[('S', 'Super'), ('M', 'Normal'), ('N', 'None')], default='M', max_length=1, verbose_name='餐补计划')),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employee.employee', verbose_name='员工')),
            ],
            options={
                'verbose_name': 'Standard Salary',
                'verbose_name_plural': 'Standard Salary',
            },
        ),
        migrations.CreateModel(
            name='SalaryDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_salary_coefficient', models.DecimalField(decimal_places=2, default=1.0, max_digits=10, verbose_name='月薪调整系数')),
                ('base_salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='月薪基数')),
                ('std_salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='定岗满勤标准月薪')),
                ('std_ensured_salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='定岗月基本工资')),
                ('std_merit_salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='定岗月基本绩效工资')),
                ('no_salary_leave_deduction', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='非带薪请假扣款')),
                ('other_salary_deduction', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='其他薪资调整减少项')),
                ('salary_increase', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='调整增加项')),
                ('salary_decrease', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='调整减少项')),
                ('total_salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='当月月薪合计')),
                ('meal_subsidy', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='餐补')),
                ('weather_subsidy', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='防暑降温福利')),
                ('rental_subsidy', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='租房补贴')),
                ('other_subsidy', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='其他福利')),
                ('total_subsidy', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='当月福利合计')),
                ('salary_before_assessment', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='考核前当月薪酬')),
                ('attendance_deduction', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='考勤考核绩效扣款')),
                ('other_assessment_deduction', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='其他考核绩效扣款')),
                ('assessment_increase', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='考核绩效增加项')),
                ('assessment_decrease', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='考核绩效减少项')),
                ('total_salary_before_tax_and_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='当月应发薪酬')),
                ('social_security_provident_fund_self_bear', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='个人承担超额缴纳部分')),
                ('total_salary_for_tax_calc', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='当月计税薪酬')),
                ('fee_self_bear', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='代扣代缴费用')),
                ('tax_self_bear', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='代扣个税')),
                ('total_salary_after_tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='当月税后薪酬')),
                ('adjustment_after_tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='税后调整')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee', verbose_name='员工')),
                ('effective_process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salary.salaryprocess', verbose_name='生效工资条')),
            ],
            options={
                'verbose_name': 'Salary Detail',
                'verbose_name_plural': 'Salary Detail',
                'unique_together': {('employee', 'effective_process')},
            },
        ),
        migrations.CreateModel(
            name='SalaryAdjustment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.CharField(choices=[('I', 'Increase'), ('D', 'Decrease')], max_length=1, verbose_name='调整方向')),
                ('adjustment_type', models.CharField(choices=[('I', 'Initial Salary'), ('S', 'Subsidy'), ('A', 'Assessment'), ('T', 'After Tax')], max_length=1, verbose_name='调整类型')),
                ('description', models.CharField(max_length=255, verbose_name='调整内容')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='金额')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee', verbose_name='员工')),
                ('effective_process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salary.salaryprocess', verbose_name='生效工资条')),
            ],
            options={
                'verbose_name': 'Salary Adjustment',
                'verbose_name_plural': 'Salary Adjustment',
                'unique_together': {('employee', 'effective_process', 'description')},
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_subsidy_state', models.CharField(choices=[('S', 'Super'), ('M', 'Normal'), ('N', 'None')], default='M', max_length=1, verbose_name='餐补级别')),
                ('work_days', models.IntegerField(verbose_name='出勤天数')),
                ('leave_days', models.IntegerField(verbose_name='非带薪请假天数')),
                ('late_times', models.IntegerField(verbose_name='迟到次数')),
                ('early_leave_times', models.IntegerField(verbose_name='早退次数')),
                ('punch_in_missing_times', models.IntegerField(verbose_name='上班缺卡次数')),
                ('punch_out_missing_times', models.IntegerField(verbose_name='下班缺卡次数')),
                ('absent_times', models.IntegerField(verbose_name='旷工天数')),
                ('no_salary_leave_duration', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='事假')),
                ('illness_leave_duration', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='病假')),
                ('employee', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='employee.employee', verbose_name='员工')),
                ('effective_process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salary.salaryprocess', verbose_name='生效工资条')),
            ],
            options={
                'verbose_name': 'Attendance',
                'verbose_name_plural': 'Attendance',
                'unique_together': {('employee', 'effective_process')},
            },
        ),
        migrations.CreateModel(
            name='SocialSecurityProvidentFund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_security_base_self_declare', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='个人申报社保基数')),
                ('social_security_amount_self_declare', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='个人承担社保金额')),
                ('social_security_amount_company_bear', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='公司承担社保金额')),
                ('social_security_additional_amount_self_bear', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='个人承担超额社保金额')),
                ('provident_fund_base_self_declare', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='个人申报公积金基数')),
                ('provident_fund_amount_self_declare', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='个人承担公积金金额')),
                ('provident_fund_amount_company_bear', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='公司承担公积金金额')),
                ('provident_fund_additional_amount_self_bear', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='个人承担超额公积金金额')),
                ('effective_process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salary.salaryprocess', verbose_name='生效工资条')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee', verbose_name='员工')),
            ],
            options={
                'verbose_name': 'Social Security Provident Fund',
                'verbose_name_plural': 'Social Security Provident Fund',
                'unique_together': {('employee', 'effective_process')},
            },
        ),
        migrations.CreateModel(
            name='Subsidy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_subsidy_plan', models.CharField(choices=[('S', 'Super'), ('M', 'Normal'), ('N', 'None')], default='M', max_length=1, verbose_name='餐补计划')),
                ('other_subsidy', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='其他福利')),
                ('effective_process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salary.salaryprocess', verbose_name='生效工资条')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee', verbose_name='员工')),
            ],
            options={
                'verbose_name': 'Subsidy',
                'verbose_name_plural': 'Subsidy',
                'unique_together': {('employee', 'effective_process')},
            },
        ),
    ]