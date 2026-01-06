from django.db import models
from apps.catalogue.models import TypeHabit


class Modele(models.Model):
    DIFFICULTE_CHOICES = [
        ('facile', 'Facile'),
        ('moyen', 'Moyen'),
        ('difficile', 'Difficile'),
    ]
    
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    type_habit = models.ForeignKey(TypeHabit, on_delete=models.CASCADE, related_name='modeles')
    difficulte = models.CharField(max_length=20, choices=DIFFICULTE_CHOICES, default='moyen')
    temps_realisation_heures = models.IntegerField(default=4)
    prix_main_oeuvre = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='modeles/', blank=True, null=True)
    description_technique = models.TextField(blank=True, null=True, help_text="Détails de confection, mesures...")
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Modèle"
        verbose_name_plural = "Modèles"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.nom} ({self.type_habit})"
