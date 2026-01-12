from django.db import models

class TypeHabit(models.Model):
    nom = models.CharField(max_length=50, unique=True)  # Chemise, Pantalon, Robe, etc.
    description = models.TextField(blank=True, null=True)
    prix_standard = models.DecimalField(max_digits=10, decimal_places=0)
    image = models.ImageField(upload_to='catalogue/habits/', blank=True, null=True)

    class Meta:
        verbose_name = "Type d'habit"
        verbose_name_plural = "Types d'habits"
        ordering = ['nom']

    def __str__(self):
        return self.nom
