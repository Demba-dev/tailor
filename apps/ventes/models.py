from django.db import models
from apps.clients.models import Client

class Vente(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventes')
    date_vente = models.DateTimeField(auto_now_add=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=0)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date_vente']
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"

    def __str__(self):
        return f"Vente #{self.pk} - {self.date_vente.strftime('%d/%m/%Y')}"

class LigneVente(models.Model):
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name='lignes')
    article_nom = models.CharField(max_length=255)
    article_type = models.CharField(max_length=50) # habit, modele, tissu
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=0)
    quantite = models.PositiveIntegerField(default=1)
    sous_total = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"{self.article_nom} x {self.quantite}"
