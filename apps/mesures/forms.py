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
            'tour_hanche',
            'epaule',
            'longueur_dos',
            'manche_longue',
            'manche_courte',
            'tour_bras',
            'longueur_jambe',
            'tour_cuisse',
            'tour_mollet',
            'longueur_pantalon',
            'encolure',
            'hauteur_poitrine',
            'largeur_dos',
            'tour_poignet',
            'hauteur_genou',
            'date_prise_mesure',
            'mesureur',
            'longueur_bras',
            'hauteur_taille',
            'largeur_epaule',
            'longueur_epaule',
            'note',
        ]
        widgets = {
            'note': forms.Textarea(attrs={'rows': 2}),
            'date_prise_mesure': forms.DateInput(attrs={'type': 'date'}),
        }
