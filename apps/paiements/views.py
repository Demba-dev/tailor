from django.shortcuts import render, redirect, get_object_or_404
from .models import Paiement
from .forms import PaiementForm
from apps.commandes.models import Commande
from django.http import JsonResponse
from django.views.decorators.http import require_GET

def paiement_list(request):
    paiements = Paiement.objects.all()
    return render(request, 'paiements/paiement_list.html', {'paiements': paiements})



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

