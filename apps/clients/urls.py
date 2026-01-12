from django.urls import path
from .views.client_views import (
    client_list,
    client_detail,
    client_create,
    client_update,
    client_delete,
    send_message
)
from . import views

app_name = 'clients'

urlpatterns = [
    path('', client_list, name='client_list'),
    path('add/', client_create, name='client_create'),
    path('<int:pk>/', client_detail, name='client_detail'),
    path('<int:pk>/edit/', client_update, name='client_update'),
    path('<int:pk>/delete/', client_delete, name='client_delete'),
    path('<int:pk>/send-message/', send_message, name='send_message'),
    path('api/search/', views.search_clients, name='search_clients'),
]
