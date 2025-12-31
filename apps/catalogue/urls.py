from django.urls import path
from .views import catalogue_list, catalogue_detail, catalogue_import, catalogue_create, add_to_favorites

app_name = 'catalogue'

urlpatterns = [
    path('', catalogue_list, name='catalogue_list'),
    path('create/', catalogue_create, name='catalogue_create'),
    path('<int:pk>/', catalogue_detail, name='catalogue_detail'),
    path('import/', catalogue_import, name='catalogue_import'),
    path('<int:pk>/add-to-favorites/', add_to_favorites, name='add_to_favorites'),
]