from django.urls import path
from . import views

app_name = 'panier'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<str:item_type>/<int:item_id>/', views.cart_add, name='cart_add'),
    path('remove/<str:item_key>/', views.cart_remove, name='cart_remove'),
    path('clear/', views.cart_clear, name='cart_clear'),
    path('api/update-quantity/', views.update_quantity, name='update_quantity'),
    path('api/remove-item/', views.remove_item, name='remove_item'),
    path('api/clear-cart/', views.clear_cart, name='clear_cart'),
]
