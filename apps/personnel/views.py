from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Personnel
from .forms import PersonnelForm

from apps.commandes.models import Commande

@login_required
def personnel_list(request):
    personnels = Personnel.objects.all()
    couturiers_count = personnels.filter(role='couturier').count()
    apprentis_count = personnels.filter(role='apprenti').count()
    active_personnel = personnels.filter(is_active=True).count()
    
    total_commandes = Commande.objects.count()
    if active_personnel > 0:
        commandes_moyennes = total_commandes / active_personnel
    else:
        commandes_moyennes = 0

    context = {
        'personnels': personnels,
        'couturiers_count': couturiers_count,
        'apprentis_count': apprentis_count,
        'active_personnel': active_personnel,
        'commandes_moyennes': commandes_moyennes,
    }
    return render(request, 'personnel/personnel_list.html', context)



@login_required
def personnel_create(request):
    if request.method == 'POST':
        form = PersonnelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('personnel:personnel_list')
    else:
        form = PersonnelForm()
    return render(request, 'personnel/personnel_form.html', {'form': form, 'title': 'Ajouter un employé'})



@login_required
def personnel_update(request, pk):
    personnel = get_object_or_404(Personnel, pk=pk)
    if request.method == 'POST':
        form = PersonnelForm(request.POST, request.FILES, instance=personnel)
        if form.is_valid():
            form.save()
            return redirect('personnel:personnel_list')
    else:
        form = PersonnelForm(instance=personnel)
    return render(request, 'personnel/personnel_form.html', {'form': form, 'title': 'Modifier employé'})



@login_required
def personnel_delete(request, pk):
    personnel = get_object_or_404(Personnel, pk=pk)
    personnel.delete()
    return redirect('personnel:personnel_list')


@login_required
def personnel_detail(request, pk):
    personnel = get_object_or_404(Personnel, pk=pk)
    return render(request, 'personnel/personnel_detail.html', {'personnel': personnel})


@login_required
def personnel_assign(request, pk):
    personnel = get_object_or_404(Personnel, pk=pk)
    if request.method == 'POST':
        formation_id = request.POST.get('formation_id')
        from apps.formations.models import Formation
        formation = get_object_or_404(Formation, pk=formation_id)
        formation.participants.add(personnel)
        return redirect('personnel:personnel_detail', pk=pk)
    
    from apps.formations.models import Formation
    formations = Formation.objects.all()
    return render(request, 'personnel/personnel_assign.html', {
        'personnel': personnel,
        'formations': formations
    })


@login_required
def personnel_schedule(request, pk):
    personnel = get_object_or_404(Personnel, pk=pk)
    if request.method == 'POST':
        form = PersonnelForm(request.POST, request.FILES, instance=personnel)
        if form.is_valid():
            form.save()
            return redirect('personnel:personnel_detail', pk=pk)
    else:
        form = PersonnelForm(instance=personnel)
    
    return render(request, 'personnel/personnel_schedule.html', {
        'personnel': personnel,
        'form': form
    })


@login_required
def personnel_bulk_assign(request):
    if request.method == 'POST':
        personnel_ids = request.POST.getlist('personnel_ids')
        formation_id = request.POST.get('formation_id')
        
        from apps.formations.models import Formation
        formation = get_object_or_404(Formation, pk=formation_id)
        
        for personnel_id in personnel_ids:
            personnel = get_object_or_404(Personnel, pk=personnel_id)
            formation.participants.add(personnel)
        
        return redirect('formations:formation_detail', pk=formation_id)
    
    personnels = Personnel.objects.all()
    from apps.formations.models import Formation
    formations = Formation.objects.all()
    
    return render(request, 'personnel/personnel_bulk_assign.html', {
        'personnels': personnels,
        'formations': formations
    })


@login_required
def personnel_report(request):
    personnels = Personnel.objects.all()
    total_personnels = personnels.count()
    personnels_actifs = personnels.filter(is_active=True).count()
    
    stats = {
        'total': total_personnels,
        'actifs': personnels_actifs,
        'inactifs': total_personnels - personnels_actifs,
        'par_role': {}
    }
    
    for role, label in Personnel.ROLE_CHOICES:
        stats['par_role'][label] = personnels.filter(role=role).count()
    
    return render(request, 'personnel/personnel_report.html', {
        'personnels': personnels,
        'stats': stats
    })
