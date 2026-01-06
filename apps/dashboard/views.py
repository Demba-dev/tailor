from django.shortcuts import render
from apps.commandes.models import Commande
from apps.paiements.models import Paiement
from apps.clients.models import Client
from apps.personnel.models import Personnel
from apps.formations.models import Formation
from django.db.models import Sum
from datetime import date

from django.urls import reverse
from apps.ventes.models import Vente

def index(request):
    commandes_encours = Commande.objects.filter(statut='encours').count()
    commandes_terminees = Commande.objects.filter(statut='termine').count()
    commandes_annulees = Commande.objects.filter(statut='annule').count()
    commandes_total = commandes_encours + commandes_terminees + commandes_annulees

    total_paiements = sum(p.montant for p in Paiement.objects.all())
    reste_total = sum(c.reste_a_payer for c in Commande.objects.all())

    total_clients = Client.objects.count()
    total_personnel = Personnel.objects.count()
    personnel_actifs = Personnel.objects.filter(is_active=True).count()
    formations_a_venir = Formation.objects.filter(statut='prevu').count()
    formations_actives = Formation.objects.exclude(statut='annulee').count()
    
    # Activités récentes
    recent_activities = []
    
    
    
    # 5 Dernières ventes
    for v in Vente.objects.order_by('-date_vente')[:5]:
        recent_activities.append({
            'title': f"Vente #{v.pk}",
            'time': v.date_vente,
            'description': f"Montant: {v.montant_total} CFA",
            'badge': 'Vente',
            'badge_color': '#10b981',
            'link': reverse('ventes:vente_detail', args=[v.pk])
        })

    # Tri par date (on convertit tout en date pour la comparaison si nécessaire)
    from datetime import datetime
    recent_activities.sort(
        key=lambda x: x['time'].date() if isinstance(x['time'], datetime) else x['time'], 
        reverse=True
    )
    recent_activities = recent_activities[:8] # On garde les 8 derniers

    # Calculer le taux de satisfaction (pourcentage de commandes terminées)
    taux_satisfaction = round((commandes_terminees / commandes_total * 100) if commandes_total > 0 else 0)
    
    # Calculer le stroke-dashoffset pour le circle de progression
    stroke_dashoffset = 251.2 - (taux_satisfaction * 2.512)
    
    # Calculer le délai moyen (en jours) pour les commandes terminées
    from django.db.models import F, ExpressionWrapper, fields
    from django.utils import timezone
    commandes_terminees_list = Commande.objects.filter(statut='termine')
    delai_moyen = 0
    if commandes_terminees_list.exists():
        total_delai = sum([
            (c.date_livraison - c.date_commande).days 
            for c in commandes_terminees_list 
            if c.date_livraison and c.date_commande
        ])
        count = sum(1 for c in commandes_terminees_list if c.date_livraison and c.date_commande)
        delai_moyen = round(total_delai / count) if count > 0 else 0
    
    # Calculer le taux de satisfaction (pourcentage de commandes livrées à temps)
    from datetime import timedelta
    commandes_livrees_a_temps = 0
    total_commandes_livrees = commandes_terminees
    
    if total_commandes_livrees > 0:
        for c in Commande.objects.filter(statut='termine'):
            if c.date_livraison and c.date_commande:
                # Considérer qu'une commande est à temps si elle est livrée dans délai_moyen + 5 jours
                if (c.date_livraison - c.date_commande).days <= (delai_moyen + 5):
                    commandes_livrees_a_temps += 1
        satisfaction_rate = round((commandes_livrees_a_temps / total_commandes_livrees * 100)) if total_commandes_livrees > 0 else 0
    else:
        satisfaction_rate = 100

    # Commandes en retard (En cours et date livraison dépassée)
    commandes_retard = Commande.objects.filter(
        statut='encours', 
        date_livraison__lt=date.today()
    ).count()

    # 5 Dernières commandes pour le tableau
    recent_orders = Commande.objects.order_by('-date_commande')[:5]

    context = {
        'commandes_encours': commandes_encours,
        'commandes_terminees': commandes_terminees,
        'commandes_annulees': commandes_annulees,
        'commandes_retard': commandes_retard,
        'recent_orders': recent_orders,
        'total_paiements': total_paiements,
        'reste_total': reste_total,
        'total_clients': total_clients,
        'total_personnel': total_personnel,
        'personnel_actifs': personnel_actifs,
        'formations_a_venir': formations_a_venir,
        'formations_actives': formations_actives,
        'taux_satisfaction': taux_satisfaction,
        'stroke_dashoffset': round(stroke_dashoffset, 2),
        'delai_moyen': delai_moyen,
        'satisfaction_rate': satisfaction_rate,
        'recent_activities': recent_activities,
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
