from django.urls import path
from . import views

app_name = 'ventes'

urlpatterns = [
    path('', views.vente_list, name='vente_list'),
    path('valider/', views.valider_vente, name='valider_vente'),
    path('<int:pk>/', views.vente_detail, name='vente_detail'),
]
