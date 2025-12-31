from django.shortcuts import render
from apps.commandes.models import Commande
from apps.paiements.models import Paiement
from apps.clients.models import Client
from apps.personnel.models import Personnel
from apps.formations.models import Formation
from django.db.models import Sum
from datetime import date

def index(request):
    commandes_encours = Commande.objects.filter(statut='encours').count()
    commandes_terminees = Commande.objects.filter(statut='termine').count()
    commandes_annulees = Commande.objects.filter(statut='annule').count()

    total_paiements = sum(p.montant for p in Paiement.objects.all())
    reste_total = sum(c.reste_a_payer for c in Commande.objects.all())

    total_clients = Client.objects.count()
    total_personnel = Personnel.objects.count()
    formations_a_venir = Formation.objects.filter(statut='prevu').count()

    context = {
        'commandes_encours': commandes_encours,
        'commandes_terminees': commandes_terminees,
        'commandes_annulees': commandes_annulees,
        'total_paiements': total_paiements,
        'reste_total': reste_total,
        'total_clients': total_clients,
        'total_personnel': total_personnel,
        'formations_a_venir': formations_a_venir,
    }
    return render(request, 'dashboard/index.html', context)

def ventes_mensuelles(request):
    today = date.today()
    commandes = Commande.objects.filter(date_commande__year=today.year, date_commande__month=today.month)
    total_ventes = commandes.aggregate(Sum('prix_total'))['prix_total__sum'] or 0
    total_reste = commandes.aggregate(Sum('reste_a_payer'))['reste_a_payer__sum'] or 0
    context = {
        'commandes': commandes,
        'total_ventes': total_ventes,
        'total_reste': total_reste,
    }
    return render(request, 'dashboard/rapports/ventes_mensuelles.html', context)
