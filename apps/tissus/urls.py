from django.urls import path
from .views import tissu_list, tissu_detail, tissu_create, tissu_update, tissu_delete

app_name = 'tissus'

urlpatterns = [
    path('', tissu_list, name='tissu_list'),
    path('ajouter/', tissu_create, name='tissu_create'),
    path('<int:pk>/', tissu_detail, name='tissu_detail'),
    path('<int:pk>/modifier/', tissu_update, name='tissu_update'),
    path('<int:pk>/supprimer/', tissu_delete, name='tissu_delete'),
]
