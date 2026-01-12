from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from apps.clients.models import Client
from apps.clients.forms import ClientForm


from django.db.models import Sum, Avg
from apps.commandes.models import Commande

def client_list(request):
    """Liste des clients actifs avec statistiques globales."""
    clients = Client.objects.filter(is_active=True)
    today = date.today()
    
    clients_actifs_mois = clients.filter(
        commandes__date_commande__month=today.month,
        commandes__date_commande__year=today.year
    ).distinct()

    total_commandes_encours = Commande.objects.filter(statut='encours').count()
    
    total_ca = Commande.objects.aggregate(total=Sum('prix_total'))['total'] or 0
    ca_moyen = total_ca / clients.count() if clients.exists() else 0

    return render(request, 'clients/client_list.html', {
        'clients': clients,
        'clients_actifs_mois': clients_actifs_mois,
        'total_commandes_encours': total_commandes_encours,
        'ca_moyen': ca_moyen
    })


def client_detail(request, pk):
    """Détail d'un client."""
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'clients/client_detail.html', {'client': client})


@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Client créé avec succès.")
            return redirect('clients:client_list')
    else:
        form = ClientForm()

    return render(request, 'clients/client_form.html', {
        'form': form,
        'title': 'Ajouter un client'
    })


@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client modifié avec succès.")
            return redirect('clients:client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)

    return render(request, 'clients/client_form.html', {
        'form': form,
        'title': 'Modifier le client'
    })

@login_required
def send_message(request, pk):
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        messages.success(request, f"Message envoyé avec succès à {client.prenom} {client.nom}.")
        
    return redirect('clients:client_detail', pk=pk)


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.is_active = False
    client.save()
    messages.success(request, f"Client {client.prenom} {client.nom} désactivé.")
    return redirect('clients:client_list')
