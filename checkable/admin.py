from django.contrib import admin

# Register your models here.

from django.http import HttpResponseRedirect
from .models import ChangeLog
from django.contrib.contenttypes.models import ContentType
from .models import Employee, AnotherModel
class VerifiableAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if '_saveandverify' in request.POST:
            obj.is_verified = True
            obj.save()  # 先保存以确保修改历史已记录
            ChangeLog.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.pk, is_verified=False).update(is_verified=True)
        super().save_model(request, obj, form, change)

    def response_change(self, request, obj):
        if "_saveandverify" in request.POST:
            self.message_user(request, "The changes have been verified and saved successfully.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['is_verified'].disabled = True
        return form

    # class Media:
    #     js = ('admin/js/custom_verify_save.js',)  # 包含自定义JS脚本

admin.site.register(Employee, VerifiableAdmin)
admin.site.register(AnotherModel, VerifiableAdmin)

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from .models import ChangeLog, VerifiableModel

class VerifiableAdmin(admin.ModelAdmin):
    actions = ['approve_changes', 'reject_changes']

    def save_model(self, request, obj, form, change):
        if '_saveandverify' in request.POST:
            obj.is_verified = True
            obj.save()  # 先保存以确保修改历史已记录
            ChangeLog.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.pk, is_verified=False).update(is_verified=True)
        else:
            obj.is_verified = False
            obj.save()
        super().save_model(request, obj, form, change)

    def response_change(self, request, obj):
        if "_saveandverify" in request.POST:
            self.message_user(request, "The changes have been verified and saved successfully.")
            return HttpResponseRedirect(".")
        elif "_reject" in request.POST:
            # 获取变更日志对象并调用其 revert_changes 方法
            content_type = ContentType.objects.get_for_model(obj)
            changelog_entries = ChangeLog.objects.filter(content_type=content_type, object_id=obj.pk, is_verified=False)
            for log in changelog_entries:
                log.content_object.revert_changes()
            changelog_entries.delete()
            self.message_user(request, "The changes have been reverted successfully.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['is_verified'].disabled = True
        return form

    def approve_changes(self, request, queryset):
        for obj in queryset:
            obj.is_verified = True
            obj.save()
            ChangeLog.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.pk, is_verified=False).update(is_verified=True)
        self.message_user(request, "Selected changes have been approved successfully.")

    approve_changes.short_description = "Approve selected changes"

    def reject_changes(self, request, queryset):
        for obj in queryset:
            obj.revert_changes()
            ChangeLog.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.pk, is_verified=False).delete()
        self.message_user(request, "Selected changes have been rejected and reverted successfully.")

    reject_changes.short_description = "Reject selected changes"

admin.site.register(ChangeLog, VerifiableAdmin)


class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'field_name', 'old_value', 'new_value', 'is_verified', 'timestamp')
    list_filter = ('is_verified', 'timestamp')
    actions = ['mark_as_verified']

    def mark_as_verified(self, request, queryset):
        # 更新选中条目的 is_verified 字段为 True
        queryset.update(is_verified=True)
        # 更新与这些 ChangeLog 条目相关的对象的 is_verified 字段
        for log in queryset:
            obj = log.content_object
            content_type = ContentType.objects.get_for_model(obj)
            # 检查是否所有变更条目都已核验
            if not ChangeLog.objects.filter(content_type=content_type, object_id=obj.pk, is_verified=False).exists():
                obj.is_verified = True
                obj.save()
        self.message_user(request, "Selected changes have been marked as verified.")

    mark_as_verified.short_description = "Mark selected changes as verified"

# admin.site.register(ChangeLog, ChangeLogAdmin)
