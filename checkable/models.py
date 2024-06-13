from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.models import ContentType

class VerifiableModel(models.Model):
    is_verified = models.BooleanField(default=False, verbose_name='Verified')
    fields_to_verify = []  # 需要核验的字段列表

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk is not None:  # 对于已存在的条目，检查需要核验的字段
            original = self.__class__.objects.get(pk=self.pk)
            for field_name in self.fields_to_verify:
                if getattr(original, field_name) != getattr(self, field_name):
                    ChangeLog.objects.create(
                        content_type=ContentType.objects.get_for_model(self),
                        object_id=self.pk,
                        field_name=field_name,
                        action='update',
                        old_value=str(getattr(original, field_name)),
                        new_value=str(getattr(self, field_name)),
                        is_verified=False
                    )
                    self.is_verified = False  # 标记条目为未核验
        else:
            super().save(*args, **kwargs)  # 先保存以生成主键
            ChangeLog.objects.create(
                content_type=ContentType.objects.get_for_model(self),
                object_id=self.pk,
                action='add',
                is_verified=False
            )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        ChangeLog.objects.create(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk,
            action='delete',
            old_value=str(self),
            is_verified=False
        )
        super().delete(*args, **kwargs)

    def revert_changes(self):
        logs = ChangeLog.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.pk, is_verified=False)
        for log in logs:
            if log.action == 'update':
                setattr(self, log.field_name, log.old_value)
        self.save()

from django.contrib.contenttypes.fields import GenericForeignKey

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class ChangeLog(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    field_name = models.CharField(max_length=255, blank=True, null=True)
    action = models.CharField(max_length=20)  # 'add', 'update', 'delete'
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.action.capitalize()} on {self.content_object}'


class Employee(VerifiableModel):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    # 其他字段...

    fields_to_verify = ['department', 'salary']  # 需要核验的字段

    def __str__(self):
        return self.name

class AnotherModel(VerifiableModel):
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField()
    # 其他字段...

    fields_to_verify = ['field1']  # 需要核验的字段
