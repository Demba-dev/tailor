from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.panier.cart import Cart
from .models import Vente, LigneVente
from apps.clients.models import Client
from django.db.models import Sum, Count, F, Max
from django.utils import timezone
from django.db.models.functions import TruncDate, Extract 

@login_required
def vente_list(request):
    ventes = Vente.objects.all()

    


    montant_total = ventes.aggregate(Sum('montant_total'))['montant_total__sum'] or 0
    
    now = timezone.now()
    month = request.GET.get('month', now.month)
    year = request.GET.get('year', now.year)
    
    try:
        month = int(month)
        year = int(year)
        if not (1 <= month <= 12):
            month = now.month
    except ValueError:
        month = now.month
        year = now.year
    
    ventes_mois_qs = ventes.filter(date_vente__month=month, date_vente__year=year)
    montant_ventes_mois = ventes_mois_qs.aggregate(Sum('montant_total'))['montant_total__sum'] or 0
    
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    ventes_dernier_mois_qs = ventes.filter(date_vente__month=prev_month, date_vente__year=prev_year)
    montant_dernier_mois = ventes_dernier_mois_qs.aggregate(Sum('montant_total'))['montant_total__sum'] or 0
    
    evolution_mensuelle = 0
    if montant_dernier_mois > 0:
        evolution_mensuelle = ((montant_ventes_mois - montant_dernier_mois) / montant_dernier_mois) * 100
    
    ventes_aujourdhui_qs = ventes.filter(date_vente__date=now.date())
    montant_ventes_aujourdhui = ventes_aujourdhui_qs.aggregate(Sum('montant_total'))['montant_total__sum'] or 0
    ventes_count_aujourdhui = ventes_aujourdhui_qs.count()
    
    total_transactions = ventes.count()
    panier_moyen = montant_total / total_transactions if total_transactions > 0 else 0
    
    meilleur_jour = None
    if ventes.exists():
        meilleur_jour_data = ventes.values('date_vente__date').annotate(
            total=Sum('montant_total'),
            count=Count('id')
        ).order_by('-total').first()
        
        if meilleur_jour_data:
            meilleur_jour = {
                'date': meilleur_jour_data['date_vente__date'],
                'total': meilleur_jour_data['total'],
                'count': meilleur_jour_data['count']
            }
    
    top_client = None
    if ventes.filter(client__isnull=False).exists():
        top_client_data = ventes.filter(client__isnull=False).values('client__prenom', 'client__nom').annotate(
            total_achats=Sum('montant_total'),
            count=Count('id')
        ).order_by('-total_achats').first()
        
        if top_client_data:
            top_client = {
                'nom_complet': f"{top_client_data['client__prenom']} {top_client_data['client__nom']}",
                'total_achats': top_client_data['total_achats'],
                'count': top_client_data['count']
            }
    
    heure_pointe = None
    if ventes.exists():
        heure_pointe_data = ventes.annotate(
            heure=Extract('date_vente', 'hour')
        ).values('heure').annotate(
            nombre_ventes=Count('id')
        ).order_by('-nombre_ventes').first()
        
        if heure_pointe_data and heure_pointe_data['heure'] is not None:
            heure_pointe = {
                'heure': f"{heure_pointe_data['heure']:02d}:00",
                'nombre_ventes': heure_pointe_data['nombre_ventes']
            }
    
    return render(request, 'ventes/vente_list.html', {
        'ventes': ventes, 
        'montant_total': montant_total, 
        'ventes_mois': montant_ventes_mois,
        'ventes_aujourdhui': montant_ventes_aujourdhui,
        'ventes_count_aujourdhui': ventes_count_aujourdhui,
        'evolution_mensuelle': evolution_mensuelle,
        'total_transactions': total_transactions,
        'panier_moyen': panier_moyen,
        'meilleur_jour': meilleur_jour,
        'top_client': top_client,
        'heure_pointe': heure_pointe,
        'current_month': month,
        'current_year': year
        
    })

@login_required
def valider_vente(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Votre panier est vide.")
        return redirect('panier:cart_detail')
    
    if request.method == 'POST':
        client_id = request.POST.get('client', '').strip()
        note = request.POST.get('note', '').strip()
        
        client = None
        if client_id:
            try:
                client = Client.objects.get(id=client_id)
            except Client.DoesNotExist:
                messages.error(request, "Client non trouvé.")
                return redirect('ventes:valider_vente')
        
        vente = Vente.objects.create(
            client=client,
            montant_total=cart.get_total_price(),
            note=note
        )
        
        for item in cart:
            LigneVente.objects.create(
                vente=vente,
                article_nom=item['obj'].nom,
                article_type=item['type'],
                prix_unitaire=item['price'],
                quantite=item['quantity'],
                sous_total=item['total_price']
            )
            
            if item['type'] == 'tissu':
                tissu = item['obj']
                if tissu.stock_metres >= item['quantity']:
                    tissu.stock_metres -= item['quantity']
                    tissu.save()
                else:
                    tissu.stock_metres = 0
                    tissu.save()
        
        cart.clear()
        messages.success(request, "Vente validée avec succès.")
        return redirect('ventes:vente_list')
    
    clients = Client.objects.all()
    return render(request, 'ventes/valider_vente.html', {
        'cart': cart,
        'clients': clients
    })

@login_required
def vente_detail(request, pk):
    vente = get_object_or_404(Vente, pk=pk)
    
    total_achats_client = 0
    montant_total_client = 0
    
    if vente.client:
        ventes_client = Vente.objects.filter(client=vente.client)
        total_achats_client = ventes_client.count()
        montant_total_client = ventes_client.aggregate(Sum('montant_total'))['montant_total__sum'] or 0
        


    return render(request, 'ventes/vente_detail.html', {
        'vente': vente,
        'total_achats_client': total_achats_client,
        'montant_total_client': montant_total_client
    })

@login_required
def facture(request, pk):
    vente = get_object_or_404(Vente, pk=pk)
    return render(request, 'ventes/facture.html', {'vente': vente})

@login_required
def print_vente(request, pk):
    vente = get_object_or_404(Vente, pk=pk)
    return render(request, 'ventes/print_vente.html', {'vente': vente})
