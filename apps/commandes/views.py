from django.shortcuts import render, redirect, get_object_or_404
from .models import Commande
from .forms import CommandeForm
from apps.panier.cart import Cart
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET

def commande_list(request):
    commandes = Commande.objects.all()
    return render(request, 'commandes/commande_list.html', {'commandes': commandes})



def commande_create(request):
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            form.save()
            # Vider le panier si la commande vient du panier
            if request.GET.get('from_cart'):
                cart = Cart(request)
                cart.clear()
            return redirect('commandes:commande_list')
    else:
        initial = {}
        
        # Si on vient du panier, on pré-remplit avec les éléments du panier
        if request.GET.get('from_cart'):
            cart = Cart(request)
            initial['prix_total'] = cart.get_total_price()
            for item in cart:
                if item['type'] == 'habit' and not initial.get('type_habit'):
                    initial['type_habit'] = item['id']
                elif item['type'] == 'modele' and not initial.get('modele'):
                    initial['modele'] = item['id']
                elif item['type'] == 'tissu' and not initial.get('tissu'):
                    initial['tissu'] = item['id']
        else:
            # Sinon on utilise les paramètres GET classiques
            for param in ['client', 'type_habit', 'modele', 'tissu', 'mesure']:
                if request.GET.get(param):
                    initial[param] = request.GET.get(param)
                    
        form = CommandeForm(initial=initial)
    return render(request, 'commandes/commande_form.html', {'form': form, 'title': 'Nouvelle commande'})



def commande_update(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('commandes:commande_list')
    else:
        form = CommandeForm(instance=commande)
    return render(request, 'commandes/commande_form.html', {'form': form, 'title': 'Modifier commande'})

def commande_detail(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    return render(request, 'commandes/commande_detail.html', {'commande': commande})



def commande_delete(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    commande.delete()
    return redirect('commandes:commande_list')


def commande_print(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    return render(request, 'commandes/commande_print.html', {'commande': commande})

def commande_duplicate(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    commande.pk = None
    commande.save()
    messages.success(request, 'Commande dupliquée avec succès')
    return redirect('commandes:commande_list')

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
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})