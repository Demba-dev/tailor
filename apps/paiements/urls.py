from django.urls import path
from .views import paiement_list, paiement_create, paiement_delete, get_commande_details, paiement_detail, paiement_print, paiement_stats, paiement_update

app_name = 'paiements'

urlpatterns = [
    path('', paiement_list, name='paiement_list'),
    path('ajouter/', paiement_create, name='paiement_create'),
    path('<int:pk>/modifier/', paiement_update, name='paiement_update'),
    path('stats/', paiement_stats, name='paiement_stats'),
    path('<int:pk>/supprimer/', paiement_delete, name='paiement_delete'),
    path('api/commande/<int:pk>/details/', get_commande_details, name='get_commande_details'),
    path('<int:pk>/', paiement_detail, name='paiement_detail'),
    path('<int:pk>/imprimer/', paiement_print, name='paiement_print'),

]
