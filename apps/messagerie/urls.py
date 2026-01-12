from django.urls import path
from . import views

app_name = 'messagerie'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('sent/', views.sent_messages, name='sent_messages'),
    path('compose/', views.compose, name='compose'),
    path('<int:pk>/', views.message_detail, name='message_detail'),
    path('message/<int:pk>/mark-read/', views.mark_message_read, name='mark_read'),
    path('message/<int:pk>/archive/', views.archive_message, name='archive_message'),
    path('message/<int:pk>/delete/', views.delete_message, name='delete_message'),
]
