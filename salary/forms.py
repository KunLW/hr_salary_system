from django import forms
from django.forms import ModelForm
from django.core.validators import validate_email
from .models import *
from employee.models import Company
class MultiEmailField(forms.Field):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(",")

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        for email in value:
            validate_email(email)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    recipients = MultiEmailField()
    cc_myself = forms.BooleanField(required=False)

class SalaryRuleForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all())
    super_meal_subsidy = forms.DecimalField(max_digits=8, decimal_places=2)
    normal_meal_subsidy = forms.DecimalField(max_digits=8, decimal_places=2)
    no_meal_subsidy = forms.DecimalField(max_digits=8, decimal_places=2)
    social_security_company_bear_base = forms.DecimalField(max_digits=10, decimal_places=2)
    social_security_company_rate = forms.DecimalField(max_digits=8, decimal_places=2)
    social_security_self_rate = forms.DecimalField(max_digits=8, decimal_places=2)
    provident_fund_company_bear_base = forms.DecimalField(max_digits=10, decimal_places=2)
    provident_fund_company_rate = forms.DecimalField(max_digits=8, decimal_places=2)
    provident_fund_self_rate = forms.DecimalField(max_digits=8, decimal_places=2)
    score_coefficient = forms.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model = SalaryRule
        fields = '__all__'
        exclude = ['company']
        
