from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.panier.cart import Cart
from .models import Vente, LigneVente
from apps.clients.models import Client

def vente_list(request):
    ventes = Vente.objects.all()
    return render(request, 'ventes/vente_list.html', {'ventes': ventes})

def valider_vente(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Votre panier est vide.")
        return redirect('panier:cart_detail')
    
    if request.method == 'POST':
        client_id = request.POST.get('client')
        note = request.POST.get('note')
        client = None
        if client_id:
            client = get_object_or_404(Client, id=client_id)
        
        # Créer la vente
        vente = Vente.objects.create(
            client=client,
            montant_total=cart.get_total_price(),
            note=note
        )
        
        # Créer les lignes de vente
        for item in cart:
            LigneVente.objects.create(
                vente=vente,
                article_nom=item['obj'].nom,
                article_type=item['type'],
                prix_unitaire=item['price'],
                quantite=item['quantity'],
                sous_total=item['total_price']
            )
            
            # Réduction du stock pour les tissus
            if item['type'] == 'tissu':
                tissu = item['obj']
                if tissu.stock_metres >= item['quantity']:
                    tissu.stock_metres -= item['quantity']
                    tissu.save()
                else:
                    # Optionnel: on pourrait lever une erreur ou mettre le stock à 0
                    tissu.stock_metres = 0
                    tissu.save()
        
        # Vider le panier
        cart.clear()
        messages.success(request, "Vente validée avec succès et enregistrée dans l'historique.")
        return redirect('ventes:vente_list')
    
    clients = Client.objects.all()
    return render(request, 'ventes/valider_vente.html', {
        'cart': cart,
        'clients': clients
    })

def vente_detail(request, pk):
    vente = get_object_or_404(Vente, pk=pk)
    return render(request, 'ventes/vente_detail.html', {'vente': vente})
