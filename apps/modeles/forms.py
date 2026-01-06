from django import forms
from .models import Modele


class ModeleForm(forms.ModelForm):
    class Meta:
        model = Modele
        fields = ['nom', 'description', 'type_habit', 'difficulte', 'temps_realisation_heures', 
                  'prix_main_oeuvre', 'description_technique', 'image', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du modèle'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'type_habit': forms.Select(attrs={'class': 'form-select'}),
            'difficulte': forms.Select(attrs={'class': 'form-select'}),
            'temps_realisation_heures': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'prix_main_oeuvre': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'description_technique': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Détails techniques'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
