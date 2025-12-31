from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from apps.clients.models import Client
from apps.clients.forms import ClientForm


def client_list(request):
    """Liste des clients actifs."""
    clients = Client.objects.filter(is_active=True)
    return render(request, 'clients/client_list.html', {'clients': clients})


def client_detail(request, pk):
    """Détail d'un client."""
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'clients/client_detail.html', {'client': client})




def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients:client_list')
    else:
        form = ClientForm()

    return render(request, 'clients/client_form.html', {
        'form': form,
        'title': 'Ajouter un client'
    })


def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients:client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)

    return render(request, 'clients/client_form.html', {
        'form': form,
        'title': 'Modifier le client'
    })

def send_message(request, pk):
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # --- Logique d'envoi ici ---
        # Exemple : send_mail(subject, message, 'from@tailor.com', [client.email])
        # Pour l'instant, on affiche juste un message de succès
        
        messages.success(request, f"Message envoyé avec succès à {client.prenom} {client.nom}.")
        
    return redirect('clients:client_detail', pk=pk)


def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.is_active = False
    client.save()
    return redirect('clients:client_list')