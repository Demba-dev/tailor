from django.contrib import admin
from .models import Setting

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('nom_atelier', 'email', 'telephone', 'devise')
    
    def has_add_permission(self, request):
        # Singleton: don't allow adding more than one
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False
