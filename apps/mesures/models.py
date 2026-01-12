from django.db import models
from apps.clients.models import Client
from apps.catalogue.models import TypeHabit  # On créera ce modèle dans Catalogue

class Mesure(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='mesures')
    type_habit = models.ForeignKey(TypeHabit, on_delete=models.SET_NULL, null=True)
    date_mesure = models.DateField(auto_now_add=True)

    tour_poitrine = models.FloatField(null=True, blank=True)
    tour_taille = models.FloatField(null=True, blank=True)
    tour_hanche = models.FloatField(null=True, blank=True)
    epaule = models.FloatField(null=True, blank=True)
    longueur_dos = models.FloatField(null=True, blank=True)
    manche_longue = models.FloatField(null=True, blank=True)
    manche_courte = models.FloatField(null=True, blank=True)
    tour_bras = models.FloatField(null=True, blank=True)
    longueur_jambe = models.FloatField(null=True, blank=True)
    tour_cuisse = models.FloatField(null=True, blank=True)
    tour_mollet = models.FloatField(null=True, blank=True)
    longueur_pantalon = models.FloatField(null=True, blank=True)
    longueur_bras = models.FloatField(null=True, blank=True)
    hauteur_taille = models.FloatField(null=True, blank=True)
    largeur_epaule = models.FloatField(null=True, blank=True)
    longueur_epaule = models.FloatField(null=True, blank=True)    
    encolure = models.FloatField(null=True, blank=True)
    hauteur_poitrine = models.FloatField(null=True, blank=True)
    largeur_dos = models.FloatField(null=True, blank=True)
    tour_poignet = models.FloatField(null=True, blank=True)
    hauteur_genou = models.FloatField(null=True, blank=True)
    
    date_prise_mesure = models.DateField(null=True, blank=True)
    date_modification = models.DateField(null=True, blank=True, auto_now=True)
    mesureur = models.CharField(max_length=100, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_mesure']

    def __str__(self):
        return f"{self.client} – {self.type_habit} ({self.date_mesure})"
    
    def get_sexe_display(self):
        if self.client.genre == 'M':
            return 'Homme'
        elif self.client.genre == 'F':
            return 'Femme'
        return 'Non spécifié'
    
    @property
    def date_prise(self):
        return self.date_mesure
    
    def get_mesures_list(self):
        mesures = [
            ('Tour Poitrine', self.tour_poitrine),
            ('Tour Taille', self.tour_taille),
            ('Tour Hanche', self.tour_hanche),
            ('Épaule', self.epaule),
            ('Longueur Dos', self.longueur_dos),
            ('Manche Longue', self.manche_longue),
            ('Manche Courte', self.manche_courte),
            ('Tour Bras', self.tour_bras),
            ('Longueur Jambe', self.longueur_jambe),
            ('Tour Cuisse', self.tour_cuisse),
            ('Tour Mollet', self.tour_mollet),
            ('Longueur Pantalon', self.longueur_pantalon),
            ('Longueur Bras', self.longueur_bras),
            ('Hauteur Taille', self.hauteur_taille),
            ('Largeur Épaule', self.largeur_epaule),
            ('Longueur Épaule', self.longueur_epaule),
            ('Encolure', self.encolure),
            ('Hauteur Poitrine', self.hauteur_poitrine),
            ('Largeur Dos', self.largeur_dos),
            ('Tour Poignet', self.tour_poignet),
            ('Hauteur Genou', self.hauteur_genou),
        ]
        return [
            {'label': label, 'value': value}
            for label, value in mesures
            if value is not None
        ]
