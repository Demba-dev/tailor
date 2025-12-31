from django.urls import path
from .views import commande_list, commande_create, commande_update, commande_delete, commande_detail, commande_print, commande_duplicate

app_name = 'commandes'

urlpatterns = [
    path('', commande_list, name='commande_list'),
    path('ajouter/', commande_create, name='commande_create'),
    path('<int:pk>/', commande_detail, name='commande_detail'),
    path('<int:pk>/modifier/', commande_update, name='commande_update'),
    path('<int:pk>/imprimer/', commande_print, name='commande_print'),
    path('<int:pk>/dupliquer/', commande_duplicate, name='commande_duplicate'),
    path('<int:pk>/supprimer/', commande_delete, name='commande_delete'),
   
]
