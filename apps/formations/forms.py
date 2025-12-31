from django import forms
from .models import Formation

class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['titre', 'description', 'date_debut', 'date_fin', 'instructeur', 'participants', 'statut', 'note',
                  'prix_par_personne', 'nombre_places', 'materiel_requis', 'objectifs', 'certification_delivree',
                  'repas_inclus', 'materiel_fourni', 'support_pdf', 'image_couverture', 'duree_heures', 'duree_jours',
                  'formateur', 'lieu', 'heure_debut', 'heure_fin', 'type_formation']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'note': forms.Textarea(attrs={'rows': 2}),
            'participants': forms.CheckboxSelectMultiple(),
            'type_formation': forms.TextInput(),
        }
