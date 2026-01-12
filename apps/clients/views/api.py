from django.http import JsonResponse
from django.db.models import Q
from apps.clients.models import Client


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
    
    return JsonResponse(list(clients), safe=False)
