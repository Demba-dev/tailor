from django.db import models
from django.db.models import Q, Count, Sum
from decimal import Decimal

class Client(models.Model):
    GENRE_CHOICES = (
        ('M', 'Homme'),
        ('F', 'Femme'),
    )

    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    genre = models.CharField(
        max_length=1,
        choices=GENRE_CHOICES,
        blank=True,
        null=True
    )

    telephone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    adresse = models.TextField(blank=True)

    note = models.TextField(
        blank=True,
        help_text="Informations particulières sur le client"
    )
    profession = models.CharField(max_length=100, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    source = models.CharField(
        max_length=50,
        blank=True,
        help_text="Origine du client (recommandation, Web, publicité, etc.)"
    )
    photo = models.ImageField(upload_to='clients/', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nom', 'prenom']
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def get_commandes_count(self):
        """Retourne le nombre total de commandes"""
        return self.commandes.count()
    
    def get_commandes_encours(self):
        """Retourne le nombre de commandes en cours"""
        return self.commandes.filter(Q(statut='encours') | Q(statut='termine')).count()
    
    def get_ca_total(self):
        """Retourne le chiffre d'affaires total (prix_total des commandes)"""
        total = self.commandes.aggregate(
            total=Sum('prix_total')
        )['total']
        return total or Decimal('0.00')
    
    def get_derniere_commande(self):
        """Retourne la dernière commande du client"""
        return self.commandes.order_by('-date_commande').first()
    
    def get_total_du(self):
        """Retourne le reste à payer (dette du client)"""
        total_commandes = self.commandes.aggregate(
            total=Sum('prix_total')
        )['total'] or Decimal('0.00')
        
        total_paye = self.commandes.aggregate(
            total=Sum('paiements__montant')
        )['total'] or Decimal('0.00')
        
        return total_commandes - total_paye

    def get_status_actif(self):
        return "Actif" if self.is_active else "Inactif"

    @property
    def paiements(self):
        """Retourne tous les paiements associés aux commandes du client"""
        from apps.paiements.models import Paiement
        return Paiement.objects.filter(commande__client=self)
