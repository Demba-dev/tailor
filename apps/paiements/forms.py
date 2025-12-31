from django import forms
from .models import Paiement

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['commande', 'montant', 'mode_paiement', 'note']
        widgets = {
            'montant': forms.NumberInput(attrs={'step': '1'}),
            'note': forms.Textarea(attrs={'rows': 2}),
        }
