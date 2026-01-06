from django.db import models
from django.db.models import Sum
from apps.clients.models import Client
from apps.mesures.models import Mesure
from apps.catalogue.models import TypeHabit
from apps.modeles.models import Modele
from apps.tissus.models import Tissu
from decimal import Decimal

class Commande(models.Model):
    STATUT_CHOICES = (
        ('encours', 'En cours'),
        ('termine', 'Terminé'),
        ('livre', 'Livré'),
        ('annule', 'Annulé'),
    )

    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='commandes')
    mesure = models.ForeignKey(Mesure, on_delete=models.SET_NULL, null=True, blank=True)
    type_habit = models.ForeignKey(TypeHabit, on_delete=models.SET_NULL, null=True, blank=True)
    modele = models.ForeignKey(Modele, on_delete=models.SET_NULL, null=True, blank=True)
    tissu = models.ForeignKey(Tissu, on_delete=models.SET_NULL, null=True, blank=True)
    date_commande = models.DateField(auto_now_add=True)
    date_livraison = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='encours')

    prix_total = models.DecimalField(max_digits=10, decimal_places=0)
    avance = models.DecimalField(max_digits=10, decimal_places=0, default=0, null=True, blank=True) # type: ignore
    reste_a_payer = models.DecimalField(max_digits=10, decimal_places=0, default=0, null=True, blank=True) # type: ignore

    note = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_commande']

    def __str__(self):
        return f"Commande #{self.id} - {self.client}"

    def calculer_reste(self):
        self.reste_a_payer = self.prix_total - self.avance
        return self.reste_a_payer
        # inclure les paiements enregistrés
        total_paye += sum(p.montant for p in self.paiements.all())
        self.reste_a_payer = self.prix_total - total_paye
        self.save()
        return self.reste_a_payer
    
    def get_montant_paye(self):
        """Retourne le total des paiements reçus"""
        total = self.paiements.aggregate( # type: ignore
            total=Sum('montant')
        )['total']
        return total or Decimal('0.00')
    
    def get_reste_a_payer(self):
        """Retourne le reste à payer calculé en temps réel"""
        montant_paye = self.get_montant_paye()
        return self.prix_total - montant_paye
    

