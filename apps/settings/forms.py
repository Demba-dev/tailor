from django import forms
from .models import Setting

class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = [
            'nom_atelier', 'adresse', 'telephone', 'email', 'logo',
            'devise', 'tva', 'delai_confection_standard', 'seuil_stock_bas',
            'langue', 'theme'
        ]
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 3}),
            'nom_atelier': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'devise': forms.TextInput(attrs={'class': 'form-control'}),
            'tva': forms.NumberInput(attrs={'class': 'form-control'}),
            'delai_confection_standard': forms.NumberInput(attrs={'class': 'form-control'}),
            'seuil_stock_bas': forms.NumberInput(attrs={'class': 'form-control'}),
            'langue': forms.Select(attrs={'class': 'form-control'}),
            'theme': forms.Select(attrs={'class': 'form-control'}),
        }
