from django.urls import path
from .views import index, ventes_mensuelles

app_name = 'dashboard'

urlpatterns = [
    path('', index, name='index'),  # Page principale du tableau de bord
    path('rapports/ventes-mensuelles/', ventes_mensuelles, name='ventes_mensuelles'),
]
