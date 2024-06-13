# Generated by Django 5.0.6 on 2024-06-12 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0007_alter_salarydetail_adjustment_after_tax_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='meal_subsidy_state',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='absent_times',
            field=models.IntegerField(null=True, verbose_name='旷工天数'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='early_leave_times',
            field=models.IntegerField(null=True, verbose_name='早退次数'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='illness_leave_duration',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='病假'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='late_times',
            field=models.IntegerField(null=True, verbose_name='迟到次数'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='leave_days',
            field=models.IntegerField(null=True, verbose_name='非带薪请假天数'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='no_salary_leave_duration',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='事假'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='punch_in_missing_times',
            field=models.IntegerField(null=True, verbose_name='上班缺卡次数'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='punch_out_missing_times',
            field=models.IntegerField(null=True, verbose_name='下班缺卡次数'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='work_days',
            field=models.IntegerField(null=True, verbose_name='出勤天数'),
        ),
    ]
