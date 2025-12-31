from django import forms
from .models import Mesure

class MesureForm(forms.ModelForm):
    class Meta:
        model = Mesure
        fields = [
            'client',
            'type_habit',
            'tour_poitrine',
            'tour_taille',
            'longueur_manche',
            'longueur_bras',
            'longueur_pantalon',
            'hauteur_taille',
            'largeur_epaules',
            'longueur_epaule',
            'date_prise_mesure',
            'mesureur',
            'longueur_totale',
            'tour_hanche',
            'note',
        ]
        widgets = {
            'note': forms.Textarea(attrs={'rows': 2}),
        }
