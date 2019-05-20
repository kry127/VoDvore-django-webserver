from django import forms
from mainApp import models

class UserForm(forms.ModelForm):
    class Meta:
        model = models.user
        fields = ['user_type', 'first_name', 'last_name', 'patronic_name', 'document_number']