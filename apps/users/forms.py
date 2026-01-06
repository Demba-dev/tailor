from django import forms
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelTypeForm if hasattr(forms, 'ModelTypeForm') else forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.Form):
    # À étendre si vous avez un modèle Profile lié
    pass
