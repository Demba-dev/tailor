from django.urls import path
from .views import (
    formation_list, formation_create, formation_update, formation_delete,
    formation_detail, formation_participants, formation_bulk_create, formation_template
)

app_name = 'formations'

urlpatterns = [
    path('', formation_list, name='formation_list'),
    path('ajouter/', formation_create, name='formation_create'),
    path('ajouter-multiple/', formation_bulk_create, name='formation_bulk_create'),
    path('template/', formation_template, name='formation_template'),
    path('<int:pk>/', formation_detail, name='formation_detail'),
    path('<int:pk>/modifier/', formation_update, name='formation_update'),
    path('<int:pk>/supprimer/', formation_delete, name='formation_delete'),
    path('<int:pk>/participants/', formation_participants, name='formation_participants'),
]
