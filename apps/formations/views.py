from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Formation
from .forms import FormationForm
from apps.personnel.models import Personnel

@login_required
def formation_list(request):
    formations = Formation.objects.all()
    context = {
        'formations': formations,
        'formations_planifiees': formations.filter(statut='prevu'),
        'formations_encours': formations.filter(statut='encours'), # Au cas où on ajoute ce statut
        'formations_terminees': formations.filter(statut='terminee'),
        'formations_annulees': formations.filter(statut='annulee'),
    }
    return render(request, 'formations/formation_list.html', context)


@login_required
def formation_create(request):
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('formations:formation_list')
    else:
        form = FormationForm()
    return render(request, 'formations/formation_form.html', {'form': form, 'title': 'Nouvelle formation'})


@login_required
def formation_update(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        form = FormationForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            return redirect('formations:formation_list')
    else:
        form = FormationForm(instance=formation)
    return render(request, 'formations/formation_form.html', {'form': form, 'title': 'Modifier formation'})


@login_required
def formation_delete(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    formation.delete()
    return redirect('formations:formation_list')


@login_required
def formation_detail(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    participants = formation.participants.all()
    context = {
        'formation': formation,
        'participants': participants,
        'participant_count': participants.count(),
        'places_available': (formation.nombre_places or 0) - participants.count(),
    }
    return render(request, 'formations/formation_detail.html', context)


@login_required
def formation_participants(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        participant_id = request.POST.get('participant_id')
        
        if action == 'add' and participant_id:
            participant = get_object_or_404(Personnel, pk=participant_id)
            formation.participants.add(participant)
            messages.success(request, f'{participant.nom} {participant.prenom} ajouté(e) à la formation')
        
        elif action == 'remove' and participant_id:
            participant = get_object_or_404(Personnel, pk=participant_id)
            formation.participants.remove(participant)
            messages.success(request, f'{participant.nom} {participant.prenom} retiré(e) de la formation')
        
        return redirect('formations:formation_participants', pk=pk)
    
    participants = formation.participants.all()
    available_personnel = Personnel.objects.exclude(pk__in=participants.values('pk')).filter(is_active=True)
    
    context = {
        'formation': formation,
        'participants': participants,
        'available_personnel': available_personnel,
    }
    return render(request, 'formations/formation_participants.html', context)


@login_required
def formation_bulk_create(request):
    if request.method == 'POST':
        titles = request.POST.getlist('titre[]')
        dates_debut = request.POST.getlist('date_debut[]')
        dates_fin = request.POST.getlist('date_fin[]')
        
        created_count = 0
        for i in range(len(titles)):
            if titles[i] and dates_debut[i] and dates_fin[i]:
                Formation.objects.create(
                    titre=titles[i],
                    date_debut=dates_debut[i],
                    date_fin=dates_fin[i],
                )
                created_count += 1
        
        messages.success(request, f'{created_count} formation(s) créée(s) avec succès')
        return redirect('formations:formation_list')
    
    return render(request, 'formations/formation_bulk_create.html')


@login_required
def formation_template(request):
    if request.method == 'POST':
        template_name = request.POST.get('template_name')
        source_formation_id = request.POST.get('source_formation_id')
        
        if source_formation_id:
            source = get_object_or_404(Formation, pk=source_formation_id)
            source.pk = None
            source.titre = template_name or f"Copie de {source.titre}"
            source.save()
            messages.success(request, 'Formation créée à partir du template')
            return redirect('formations:formation_update', pk=source.pk)
    
    formations = Formation.objects.all()
    context = {
        'formations': formations,
    }
    return render(request, 'formations/formation_template.html', context)
