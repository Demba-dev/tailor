from django.urls import path
from .views import (
    personnel_list, personnel_create, personnel_update, personnel_delete,
    personnel_detail, personnel_assign, personnel_schedule,
    personnel_bulk_assign, personnel_report
)

app_name = 'personnel'

urlpatterns = [
    path('', personnel_list, name='personnel_list'),
    path('ajouter/', personnel_create, name='personnel_create'),
    path('<int:pk>/modifier/', personnel_update, name='personnel_update'),
    path('<int:pk>/supprimer/', personnel_delete, name='personnel_delete'),
    path('<int:pk>/', personnel_detail, name='personnel_detail'),
    path('<int:pk>/assigner/', personnel_assign, name='personnel_assign'),
    path('<int:pk>/planning/', personnel_schedule, name='personnel_schedule'),
    path('assigner-multiple/', personnel_bulk_assign, name='personnel_bulk_assign'),
    path('rapport/', personnel_report, name='personnel_report'),
]
