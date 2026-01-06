from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm

@login_required
def user_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # On suppose qu'on utilise le modèle User de base ou un profil étendu
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Votre compte a été mis à jour !')
            return redirect('users:user_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }
    return render(request, 'users/profile.html', context)
