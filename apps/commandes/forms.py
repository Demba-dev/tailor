from django import forms
from .models import Commande

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = [
            'client',
            'mesure',
            'type_habit',
            'date_livraison',
            'statut',
            'prix_total',
            'note',
        ]
        widgets = {
            'date_livraison': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 2}),
        }
