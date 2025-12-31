from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'prenom',
            'nom',
            'genre',
            'telephone',
            'email',
            'adresse',
            'note',
            'is_active',
        ]

        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 2}),
            'note': forms.Textarea(attrs={'rows': 2}),
        }
