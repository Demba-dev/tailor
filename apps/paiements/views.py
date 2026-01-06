from django.shortcuts import render, redirect, get_object_or_404
from .models import Paiement
from .forms import PaiementForm
from apps.commandes.models import Commande
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from django.db.models import Sum, Avg
from django.utils import timezone
from datetime import timedelta

def paiement_list(request):
    paiements = Paiement.objects.all()
    today = timezone.now()
    
    # Statistiques de base
    total_paiements = paiements.aggregate(Sum('montant'))['montant__sum'] or 0
    
    # Ce mois-ci
    paiements_mois = paiements.filter(date_paiement__month=today.month, date_paiement__year=today.year)
    paiements_du_mois = paiements_mois.aggregate(Sum('montant'))['montant__sum'] or 0
    paiements_mois_count = paiements_mois.count()
    
    # Mois dernier (pour évolution)
    first_day_this_month = today.replace(day=1)
    last_day_last_month = first_day_this_month - timedelta(days=1)
    paiements_mois_dernier = paiements.filter(
        date_paiement__month=last_day_last_month.month, 
        date_paiement__year=last_day_last_month.year
    ).aggregate(Sum('montant'))['montant__sum'] or 0
    
    if paiements_mois_dernier > 0:
        evolution_mensuelle = ((paiements_du_mois - paiements_mois_dernier) / paiements_mois_dernier) * 100
    else:
        evolution_mensuelle = 100 if paiements_du_mois > 0 else 0

    # Impayés
    commandes = Commande.objects.all()
    impayes = commandes.aggregate(Sum('reste_a_payer'))['reste_a_payer__sum'] or 0
    commandes_impayees = commandes.filter(reste_a_payer__gt=0).count()
    
    # Moyennes et Taux
    moyenne_paiement = paiements.aggregate(Avg('montant'))['montant__avg'] or 0
    total_commandes = commandes.count()
    commandes_payees = commandes.filter(reste_a_payer__lte=0).count()
    
    taux_paiement_complet = (commandes_payees / total_commandes * 100) if total_commandes > 0 else 0

    context = {
        'paiements': paiements,
        'total_paiements': total_paiements,
        'paiements_du_mois': paiements_du_mois,
        'paiements_mois_count': paiements_mois_count,
        'evolution_mensuelle': evolution_mensuelle,
        'impayes': impayes,
        'commandes_impayees': commandes_impayees,
        'moyenne_paiement': moyenne_paiement,
        'taux_paiement_complet': int(taux_paiement_complet),
    }
    return render(request, 'paiements/paiement_list.html', context)



def paiement_create(request):
    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            paiement = form.save()
            # Mettre à jour le reste à payer de la commande
            commande = paiement.commande
            total_paye = sum(p.montant for p in commande.paiements.all())
            commande.reste_a_payer = commande.prix_total - total_paye
            commande.save()
            return redirect('paiements:paiement_list')
    else:
        form = PaiementForm()
    return render(request, 'paiements/paiement_form.html', {'form': form, 'title': 'Nouveau paiement'})

def paiement_update(request, pk):
    paiement = get_object_or_404(Paiement, pk=pk)
    if request.method == 'POST':
        form = PaiementForm(request.POST, instance=paiement)
        if form.is_valid():
            form.save()
            return redirect('paiements:paiement_detail', pk=paiement.pk)
    else:
        form = PaiementForm(instance=paiement)
    return render(request, 'paiements/paiement_form.html', {'form': form, 'title': 'Modifier paiement'})


def paiement_stats(request):
    from django.db.models import Sum
    from apps.commandes.models import Commande
    
    total_paiements = Paiement.objects.aggregate(Sum('montant'))['montant__sum'] or 0
    total_commandes = Commande.objects.aggregate(Sum('prix_total'))['prix_total__sum'] or 0
    paiements_count = Paiement.objects.count()
    
    stats = {
        'total_paiements': int(total_paiements),
        'total_commandes': int(total_commandes),
        'paiements_count': paiements_count,
        'montant_moyen': int(total_paiements // paiements_count) if paiements_count > 0 else 0,
    }
    
    return render(request, 'paiements/paiement_stats.html', stats)



def paiement_delete(request, pk):
    paiement = get_object_or_404(Paiement, pk=pk)
    commande = paiement.commande
    paiement.delete()
    # Mettre à jour le reste à payer
    total_paye = sum(p.montant for p in commande.paiements.all()) # type: ignore
    commande.reste_a_payer = commande.prix_total - total_paye
    commande.save()
    return redirect('paiements:paiement_list')

@require_GET
def get_commande_details(request, pk):
    try:
        commande = Commande.objects.get(pk=pk)
        return JsonResponse({
            'success': True,
            'client_prenom': commande.client.prenom,
            'client_nom': commande.client.nom,
            'habit_nom': commande.type_habit.nom, # type: ignore
            'prix_total': float(commande.prix_total),
            'montant_paye': float(commande.get_montant_paye()),
            'reste_a_payer': float(commande.get_reste_a_payer()),
            'date_commande': commande.date_commande.strftime('%d/%m/%Y'),
        })
    except Commande.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Commande non trouvée'})


def paiement_detail(request, pk):
    paiement = get_object_or_404(Paiement, pk=pk)
    return render(request, 'paiements/paiement_detail.html', {'paiement': paiement})


def paiement_print(request, pk):
    paiement = get_object_or_404(Paiement, pk=pk)
    return render(request, 'paiements/paiement_print.html', {'paiement': paiement})

