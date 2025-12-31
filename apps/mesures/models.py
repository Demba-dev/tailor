from django.db import models
from apps.clients.models import Client
from apps.catalogue.models import TypeHabit  # On créera ce modèle dans Catalogue

class Mesure(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='mesures')
    type_habit = models.ForeignKey(TypeHabit, on_delete=models.SET_NULL, null=True)
    date_mesure = models.DateField(auto_now_add=True)

    # Mesures possibles (chemise/pantalon/robe)
    tour_poitrine = models.FloatField(null=True, blank=True)
    tour_taille = models.FloatField(null=True, blank=True)
    longueur_manche = models.FloatField(null=True, blank=True)
    longueur_bras = models.FloatField(null=True, blank=True)
    longueur_pantalon = models.FloatField(null=True, blank=True)
    hauteur_taille = models.FloatField(null=True, blank=True)
    largeur_epaules = models.FloatField(null=True, blank=True)
    longueur_epaule = models.FloatField(null=True, blank=True)
    date_prise_mesure = models.DateField(null=True, blank=True)
    mesureur = models.CharField(max_length=100, blank=True)
    longueur_totale = models.FloatField(null=True, blank=True)
    tour_hanche = models.FloatField(null=True, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_mesure']

    def __str__(self):
        return f"{self.client} – {self.type_habit} ({self.date_mesure})"
