from django.urls import path
from .views import modele_list, modele_detail, modele_create, modele_update, modele_delete

app_name = 'modeles'

urlpatterns = [
    path('', modele_list, name='modele_list'),
    path('ajouter/', modele_create, name='modele_create'),
    path('<int:pk>/', modele_detail, name='modele_detail'),
    path('<int:pk>/modifier/', modele_update, name='modele_update'),
    path('<int:pk>/supprimer/', modele_delete, name='modele_delete'),
]
