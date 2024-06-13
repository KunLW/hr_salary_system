# Generated by Django 5.0.6 on 2024-06-12 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salarydetail',
            name='adjustment_after_tax',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='税后调整'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='assessment_decrease',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='考核绩效减少项'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='assessment_increase',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='考核绩效增加项'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='attendance_deduction',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='考勤考核绩效扣款'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='base_salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='月薪基数'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='base_salary_coefficient',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, verbose_name='月薪调整系数'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='fee_self_bear',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='代扣代缴费用'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='meal_subsidy',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='餐补'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='no_salary_leave_deduction',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='非带薪请假扣款'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='other_assessment_deduction',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='其他考核绩效扣款'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='other_salary_deduction',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='其他薪资调整减少项'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='other_subsidy',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='其他福利'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='rental_subsidy',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='租房补贴'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='salary_before_assessment',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='考核前当月薪酬'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='salary_decrease',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='调整减少项'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='salary_increase',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='调整增加项'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='social_security_provident_fund_self_bear',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='个人承担超额缴纳部分'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='std_ensured_salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='定岗月基本工资'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='std_merit_salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='定岗月基本绩效工资'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='std_salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='定岗满勤标准月薪'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='tax_self_bear',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='代扣个税'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='total_salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='当月月薪合计'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='total_salary_after_tax',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='当月税后薪酬'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='total_salary_before_tax_and_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='当月应发薪酬'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='total_salary_for_tax_calc',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='当月计税薪酬'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='total_subsidy',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='当月福利合计'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='weather_subsidy',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='防暑降温福利'),
        ),
    ]
