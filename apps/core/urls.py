from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/mark-read/<int:pk>/', views.mark_as_read, name='mark_as_read'),
    path('notifications/mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),
]
