from django import forms
from .models import Personnel

class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = [
            'nom', 
            'prenom',
            'is_active',
            'photo',
            'email', 'telephone', 'role', 'date_embauche', 'actif', 'note',
            'genre', 'date_naissance', 'lieu_naissance', 'cni', 'numero_securite_sociale',
            'adresse', 'ville', 'code_postal', 'statut_emploi', 'niveau_etude', 'annees_experience',
            'formations_notes', 'specialites', 'notes_competences', 'jours_travail', 'heure_debut',
            'heure_fin', 'disponibilites', 'jours_conges_restants', 'jours_maladies',
            'notes_horaires', 'type_contrat', 'date_fin_contrat', 'salaire', 'prime_fixe',
            'type_salaire',]
        widgets = {
            'date_embauche': forms.DateInput(attrs={'type': 'date'}),
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'date_fin_contrat': forms.DateInput(attrs={'type': 'date'}),
            'annees_experience': forms.NumberInput(),
            'jours_conges_restants': forms.NumberInput(),
            'jours_maladies': forms.NumberInput(),
            'salaire': forms.NumberInput(),
            'prime_fixe': forms.NumberInput(),
            'type_salaire': forms.Select(choices=Personnel.TYPE_SALAIRE_CHOICES),
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
            'disponibilites': forms.TimeInput(attrs={'type': 'time'}),
            'formations_notes': forms.Textarea(attrs={'rows': 3}),
            'note': forms.Textarea(attrs={'rows': 2}),
            'photo': forms.FileInput(attrs={'accept': 'image/*'}),
            'telephone': forms.TextInput(attrs={'maxlength': 20, 'placeholder': '77 12 34 56 78'}),
        }
