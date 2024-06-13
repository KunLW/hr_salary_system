
from django.db import models
from .models import *

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import StdSalary
from employee.models import Employee, Position
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)




# @receiver(post_save, sender=Employee)
# def create_or_update_std_salary(sender, instance, created, **kwargs):
#     if instance.position is not None:
#         print("====signal triggered====")
#         if created:
#                 print(f"====creating{instance}===={instance.position.base_salary}====")
#                 StdSalary.objects.create(employee=instance, base_salary=instance.position.base_salary)
#         else:
#             std_salary, _ = StdSalary.objects.get_or_create(employee=instance)
#             std_salary.base_salary = instance.position.base_salary
#             std_salary.save()

# @receiver(post_save, sender=Position)
# def update_std_salary(sender, instance, created, **kwargs):
#     employees = Employee.objects.filter(position=instance)
#     for employee in employees:
#         std_salary, _ = StdSalary.objects.get_or_create(employee=employee)
#         std_salary.base_salary = instance.base_salary
#         std_salary.save()

# @receiver(post_save, sender=SalaryRule)
# def update_social_security(sender, instance, created, **kwargs):
#     social_securities = SocialSecurityProvidentFund.objects.all()
#     for social_security in social_securities:
#         try: 
#             social_security_amount_self_declare, social_security_amount_company_bear, social_security_additional_amount_self_bear = calculate_social_security_salary(social_security.employee)
#             social_security.social_security_amount_self_declare = social_security_amount_self_declare
#             social_security.social_security_amount_company_bear = social_security_amount_company_bear
#             social_security.social_security_additional_amount_self_bear = social_security_additional_amount_self_bear
#             social_security.save()
#         except AttributeError:
#             pass


# @receiver(pre_save, sender=SocialSecurityProvidentFund)
# def update_social_security(sender, instance, **kwargs):
#     try: 
#         social_security_amount_self_declare, social_security_amount_company_bear, social_security_additional_amount_self_bear = calculate_social_security_salary(instance.employee)
#         instance.social_security_amount_self_declare = social_security_amount_self_declare
#         instance.social_security_amount_company_bear = social_security_amount_company_bear
#         instance.social_security_additional_amount_self_bear = social_security_additional_amount_self_bear
#     except AttributeError:
#         pass
