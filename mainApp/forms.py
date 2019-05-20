from django import forms
from mainApp import models

from django.utils.translation import gettext_lazy as _

class RegisterForm(forms.ModelForm):
    class Meta:
        model = models.user
        fields = ['user_type', 'last_name', 'first_name', 'patronic_name', 'document_number', 'login', 'password']
        # TODO разобраться, как переопределить виджет
        widgets = {
            'first_name': forms.TextInput(attrs={"class":"form-control"}),
            'password': forms.PasswordInput(attrs={"class":"form-control"})
        }
        labels = {
            'first_name': _('First nameeee'),
        }
        help_texts = {
            'first_name': _('Some useful help text.'),
        }
        error_messages = {
            'first_name': {
                'max_length': _("The user name should not be empty"),
            },
        }