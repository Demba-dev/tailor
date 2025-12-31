from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'telephone', 'email', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('nom', 'prenom', 'telephone', 'email')
    ordering = ('nom', 'prenom')
    list_per_page = 20
