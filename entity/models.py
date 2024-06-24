from django.db import models
from django.contrib import auth

# Create your models here.
class Verification(models.Model):
    is_verified = models.BooleanField(default=False, verbose_name='已审核')
    verifier = models.ForeignKey(auth.user, on_delete=models.CASCADE, verbose_name='审核人', null=True, blank=True)
    verify_time = models.DateTimeField(auto_now=True, verbose_name='审核时间')
    note = models.TextField(verbose_name='审核备注', null=True, blank=True)
    is_pass = models.BooleanField(default=False, verbose_name='审核通过')
    

    class Meta:
        abstract = True
