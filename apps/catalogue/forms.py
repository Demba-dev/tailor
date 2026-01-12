from django import forms
from .models import TypeHabit


class TypeHabitForm(forms.ModelForm):
    class Meta:
        model = TypeHabit
        fields = ['nom', 'description', 'prix_standard', 'image']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Chemise, Pantalon, Robe...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description du type d\'habit'
            }),
            'prix_standard': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Prix standard en cfa'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
