from django.db import models
from apps.commandes.models import Commande

class Paiement(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='paiements')
    date_paiement = models.DateField(auto_now_add=True)
    montant = models.DecimalField(max_digits=10, decimal_places=0)
    mode_paiement = models.CharField(
        max_length=50,
        choices=(
            ('espece', 'Espèces'),
            ('carte', 'Carte bancaire'),
            ('mobile', 'Paiement mobile'),
        ),
        default='espece'
    )
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_paiement']

    def __str__(self):
        return f"{self.commande} – {self.montant}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.commande.calculer_reste()

    def get_mode_display(self):
        modes = {
            'espece': 'Espèces',
            'carte': 'Carte bancaire',
            'mobile': 'Paiement mobile'
        }
        return modes.get(self.mode_paiement, self.mode_paiement)

    @property
    def get_mode_icon(self):
        icons = {
            'espece': 'money-bill-wave',
            'carte': 'credit-card',
            'mobile': 'mobile-alt'
        }
        return icons.get(self.mode_paiement, 'coins')
