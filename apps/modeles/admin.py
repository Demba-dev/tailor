from django.contrib import admin
from .models import Modele


@admin.register(Modele)
class ModeleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_habit', 'difficulte', 'temps_realisation_heures', 'prix_main_oeuvre', 'actif')
    list_filter = ('type_habit', 'difficulte', 'actif', 'date_creation')
    search_fields = ('nom', 'type_habit', 'description')
    fieldsets = (
        ('Informations Générales', {'fields': ('nom', 'type_habit', 'description')}),
        ('Détails Techniques', {'fields': ('difficulte', 'temps_realisation_heures', 'description_technique')}),
        ('Tarification', {'fields': ('prix_main_oeuvre',)}),
        ('Média', {'fields': ('image',)}),
        ('Statut', {'fields': ('actif',)}),
    )
