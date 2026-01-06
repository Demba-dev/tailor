from django.db import models
from apps.core.models.base import TimeStampedModel

class Setting(TimeStampedModel):
    # Atelier Info
    nom_atelier = models.CharField(max_length=255, default="Mon Atelier de Couture")
    adresse = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    logo = models.ImageField(upload_to='settings/logos/', blank=True, null=True)
    
    # Paramètres Métier
    devise = models.CharField(max_length=10, default="FCFA")
    tva = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Taux de TVA en %")
    delai_confection_standard = models.IntegerField(default=7, help_text="Délai standard en jours")
    
    # Notifications
    seuil_stock_bas = models.IntegerField(default=5, help_text="Alerte stock bas (quantité)")

    # Interface
    LANGUES_CHOICES = [
        ('fr', 'Français'),
        ('en', 'English'),
    ]
    THEME_CHOICES = [
        ('light', 'Clair'),
        ('dark', 'Sombre'),
    ]
    langue = models.CharField(max_length=5, choices=LANGUES_CHOICES, default='fr')
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')

    class Meta:
        verbose_name = "Paramètres"
        verbose_name_plural = "Paramètres"

    def __str__(self):
        return self.nom_atelier

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Setting, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
