from django.urls import path
from .views import mesure_list, mesure_create, mesure_update, mesure_delete, mesure_detail, mesure_duplicate, mesure_print, mesure_import, mesure_bulk_delete

app_name = 'mesures'

urlpatterns = [
    path('', mesure_list, name='mesure_list'),
    path('client/<int:client_id>/', mesure_list, name='mesure_list_client'),
    path('ajouter/', mesure_create, name='mesure_create'),
    path('importer/', mesure_import, name='mesure_import'),
    path('<int:pk>/', mesure_detail, name='mesure_detail'),
    path('ajouter/<int:client_id>/', mesure_create, name='mesure_create_client'),
    path('<int:pk>/dupliquer/', mesure_duplicate, name='mesure_duplicate'),
    path('<int:pk>/imprimer/', mesure_print, name='mesure_print'),
    path('<int:pk>/modifier/', mesure_update, name='mesure_update'),
    path('<int:pk>/supprimer/', mesure_delete, name='mesure_delete'),
    path('supprimer-multiples/', mesure_bulk_delete, name='mesure_bulk_delete'),
]
