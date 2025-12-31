from django.contrib import admin
from .models import Personnel

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'role', 'email', 'telephone', 'is_active', 'date_embauche')
    list_filter = ('role', 'is_active', 'date_embauche')
    search_fields = ('nom', 'prenom', 'email', 'telephone')
    ordering = ('nom', 'prenom')
