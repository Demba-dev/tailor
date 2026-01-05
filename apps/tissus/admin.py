from django.contrib import admin
from .models import Tissu


@admin.register(Tissu)
class TissuAdmin(admin.ModelAdmin):
    list_display = ('nom', 'matiere', 'motif', 'couleur', 'prix_metre', 'stock_metres', 'actif')
    list_filter = ('matiere', 'motif', 'actif', 'date_ajout')
    search_fields = ('nom', 'couleur', 'description')
    fieldsets = (
        ('Informations Générales', {'fields': ('nom', 'description')}),
        ('Caractéristiques', {'fields': ('matiere', 'motif', 'couleur')}),
        ('Stock et Prix', {'fields': ('prix_metre', 'stock_metres')}),
        ('Média', {'fields': ('image',)}),
        ('Statut', {'fields': ('actif',)}),
    )
