from django.db import models
from django.contrib.auth.models import User

class Personnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='personnel_profile')
    ROLE_CHOICES = (
        ('couturier', 'Couturier'),
        ('apprenti', 'Apprenti'),
        ('contractuel', 'contractuel'),
        ('commercial', 'Commercial'),
        ('admin', 'Administratif'),
    )
    GENRE_CHOICES = (
        ('M', 'Homme'),
        ('F', 'Femme'),
    )

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    date_embauche = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True)
    genre = models.CharField(
        max_length=1,
        choices=GENRE_CHOICES,
        blank=True,
        null=True
    )
    TYPE_SALAIRE_CHOICES = (
        ('mensuel', 'Mensuel'),
        ('horaire', 'Horaire'),
    )

    date_naissance = models.DateField(blank=True, null=True)
    lieu_naissance = models.CharField(max_length=100, blank=True, null=True)
    cni = models.CharField(max_length=50, blank=True, null=True)
    numero_securite_sociale = models.CharField(max_length=50, blank=True, null=True)
    adresse = models.TextField(blank=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    code_postal = models.CharField(max_length=20, blank=True, null=True)

    type_contrat = models.CharField(max_length=100, blank=True, null=True)
    date_fin_contrat = models.DateField(blank=True, null=True)
    salaire = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    prime_fixe = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    type_salaire = models.CharField(max_length=100, blank=True, null=True)

    statut_emploi = models.CharField(max_length=100, blank=True, null=True)
    niveau_etude = models.CharField(max_length=100, blank=True, null=True)
    annees_experience = models.IntegerField(blank=True, null=True)
    formations_notes = models.CharField(blank=True, null=True)
    specialites = models.CharField(blank=True, null=True)
    notes_competences = models.CharField(blank=True, null=True)
    jours_travail = models.CharField(max_length=100, blank=True, null=True)
    heure_debut = models.TimeField(blank=True, null=True)
    heure_fin = models.TimeField(blank=True, null=True)
    disponibilites = models.TimeField(blank=True, null=True)
    jours_conges_restants = models.IntegerField(blank=True, null=True)
    jours_maladies = models.IntegerField(blank=True, null=True)
    notes_horaires = models.CharField(blank=True, null=True)
    photo = models.ImageField(upload_to='personnel/', blank=True, null=True)
    is_active = models.BooleanField(default=True)



    class Meta:
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.role})"
    
    def get_specialite_display(self):
        return self.specialites if self.specialites else "N/A" 
    
    def get_disponibilite_display(self):
        return "Disponible" if self.disponibilites else "Occupé"
