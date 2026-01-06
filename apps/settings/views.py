from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Setting
from .forms import SettingForm

@login_required
def settings_view(request):
    settings_obj = Setting.load()
    
    if request.method == 'POST':
        form = SettingForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Les paramètres ont été mis à jour avec succès.")
            return redirect('settings:settings_detail')
    else:
        form = SettingForm(instance=settings_obj)
    
    context = {
        'form': form,
        'settings_obj': settings_obj,
        'title': 'Paramètres de l\'Atelier'
    }
    return render(request, 'settings/settings_form.html', context)
