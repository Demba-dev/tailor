from django.contrib import admin
from django.utils.html import format_html
from .models import TypeHabit

@admin.register(TypeHabit)
class TypeHabitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix_standard', 'description')
    search_fields = ('nom',)
    ordering = ('nom',)
    list_per_page = 20
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" />', obj.image.url)
        return "-"
    image_preview.short_description = "Aperçu de l'image"
