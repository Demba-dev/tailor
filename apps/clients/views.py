from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Client


@login_required
def search_clients(request):
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse([])
    
    clients = Client.objects.filter(
        Q(prenom__icontains=query) |
        Q(nom__icontains=query) |
        Q(telephone__icontains=query) |
        Q(email__icontains=query),
        is_active=True
    ).values('id', 'prenom', 'nom', 'telephone', 'email')[:10]
    
    return JsonResponse(list(clients))
