from django.db import models
from apps.personnel.models import Personnel

class Formation(models.Model):
    STATUT_CHOICES = (
        ('planifiee', 'Planifiée'),
        ('encours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    )

    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    instructeur = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'is_active': True})
    participants = models.ManyToManyField(Personnel, related_name='formations', blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifiee')
    note = models.TextField(blank=True)
    prix_par_personne = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    nombre_places = models.IntegerField(blank=True, null=True)
    materiel_requis = models.TextField(blank=True)
    objectifs = models.CharField(blank=True)
    certification_delivree = models.BooleanField(default=False)
    repas_inclus = models.BooleanField(default=False)
    materiel_fourni = models.BooleanField(default=False)
    support_pdf = models.BooleanField(default=False)
    image_couverture = models.ImageField(upload_to='formations/couvertures/', blank=True, null=True)
    duree_heures = models.IntegerField(blank=True, null=True)
    duree_jours = models.IntegerField(blank=True, null=True)
    lieu = models.CharField(max_length=200, blank=True)
    heure_debut = models.TimeField(blank=True, null=True)
    heure_fin = models.TimeField(blank=True, null=True)
    type_formation = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['date_debut']

    def __str__(self):
        return f"{self.titre} ({self.date_debut} - {self.date_fin})"
