from django.db import models


class Tissu(models.Model):
    MOTIF_CHOICES = [
        ('unie', 'Unie'),
        ('rayure', 'Rayure'),
        ('carreaux', 'Carreaux'),
        ('floral', 'Floral'),
        ('autre', 'Autre'),
    ]
    
    MATIERE_CHOICES = [
        ('coton', 'Coton'),
        ('lin', 'Lin'),
        ('soie', 'Soie'),
        ('polyester', 'Polyester'),
        ('mix', 'Mix'),
    ]
    
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    matiere = models.CharField(max_length=20, choices=MATIERE_CHOICES)
    motif = models.CharField(max_length=20, choices=MOTIF_CHOICES, default='unie')
    couleur = models.CharField(max_length=50, blank=True)
    prix_metre = models.DecimalField(max_digits=10, decimal_places=2)
    stock_metres = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='tissus/', blank=True, null=True)
    actif = models.BooleanField(default=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tissu"
        verbose_name_plural = "Tissus"
        ordering = ['-date_ajout']
    
    def __str__(self):
        return f"{self.nom} ({self.matiere})"
