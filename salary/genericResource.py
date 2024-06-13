from import_export import resources, fields, widgets
from import_export.widgets import Widget

class ForeignKeyWidgetByName(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        try:
            return self.model.objects.get(name=value)
        except self.model.DoesNotExist:
            print(f"{self.model.__name__} matching query does not exist: {value}")
            return None
        
    def render(self, value, obj=None):
        if value is None:
            return ""
        return getattr(value, self.field, None)

class ChoiceDisplayWidget(widgets.Widget):
    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = choices

    def clean(self, value, row=None, *args, **kwargs):
        for choice_value, choice_display in self.choices:
            if choice_display == value:
                return choice_value
        return None

    def render(self, value, obj=None):
        for choice_value, choice_display in self.choices:
            if value == choice_value:
                return choice_display
        return None
from import_export.widgets import ForeignKeyWidget

from django.db import models
from django.utils.encoding import force_str
class GenericModelResource(resources.ModelResource):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.get_fields():
            field_name = self.get_field_name(field)
            verbose_name = model._meta.get_field(field_name).verbose_name
            
            model_field = model._meta.get_field(field_name)
            
            if isinstance(field, fields.Field):
                if isinstance(model_field, models.ForeignKey):
                    original_widget = field.widget
                    # original_widget = ForeignKeyWidget(model_field.related_model, 'name')
                    # original_widget = ForeignKeyRawIdWidget(model_field.remote_field, self.admin_site)
                elif model_field.choices:
                    original_widget = ChoiceDisplayWidget(model_field.choices)
                else:
                    original_widget = field.widget
            else:
                original_widget = widgets.Widget()
            
            self.fields[field_name] = fields.Field(attribute=field_name, 
                                                   column_name=force_str(verbose_name), 
                                                   widget=original_widget)
    
    # def get_field_name(self, field):
    #     return field.attribute or field.column_name

    # def get_fields(self):
    #     return self.fields.values()
    
    def skip_row(self, instance, original, row, import_validation_errors=None):
        if all(value in [None, ""] for value in row.values()):
            print("an empty input found")
            return True
        return super().skip_row(instance, original, row, import_validation_errors=import_validation_errors)
    


class GenericModelActionResource(resources.ModelResource):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.get_fields():
            field_name = self.get_field_name(field)
            verbose_name = model._meta.get_field(field_name).verbose_name
            
            model_field = model._meta.get_field(field_name)
            
            if isinstance(field, fields.Field):
                if isinstance(model_field, models.ForeignKey):
                    original_widget = ForeignKeyWidget(model_field.related_model, 'name')
                    # original_widget = field.widget
                elif model_field.choices:
                    original_widget = ChoiceDisplayWidget(model_field.choices)
                else:
                    original_widget = field.widget
            else:
                original_widget = widgets.Widget()
            
            self.fields[field_name] = fields.Field(attribute=field_name, 
                                                   column_name=force_str(verbose_name), 
                                                   widget=original_widget)
    
    # def get_field_name(self, field):
    #     return field.attribute or field.column_name

    # def get_fields(self):
    #     return self.fields.values()
    
    def skip_row(self, instance, original, row, import_validation_errors=None):
        if all(value in [None, ""] for value in row.values()):
            print("an empty input found")
            return True
        return super().skip_row(instance, original, row, import_validation_errors=import_validation_errors)
    
