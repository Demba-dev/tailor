from django.shortcuts import render, get_object_or_404, redirect
from .models import Modele
from .forms import ModeleForm
from apps.catalogue.models import TypeHabit
from django.contrib import messages


def modele_list(request):
    modeles = Modele.objects.filter(actif=True)
    type_filter = request.GET.get('type')
    difficulte_filter = request.GET.get('difficulte')
    search = request.GET.get('search')
    
    if type_filter:
        modeles = modeles.filter(type_habit__pk=type_filter)
    if difficulte_filter:
        modeles = modeles.filter(difficulte=difficulte_filter)
    if search:
        modeles = modeles.filter(nom__icontains=search)
    
    context = {
        'modeles': modeles,
        'difficultes': Modele.DIFFICULTE_CHOICES,
        'type_habits': TypeHabit.objects.all(),
    }
    return render(request, 'modeles/modele_list.html', context)


def modele_detail(request, pk):
    modele = get_object_or_404(Modele, pk=pk)
    context = {'modele': modele}
    return render(request, 'modeles/modele_detail.html', context)


def modele_create(request):
    if request.method == 'POST':
        form = ModeleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modèle ajouté avec succès')
            return redirect('modeles:modele_list')
    else:
        form = ModeleForm()
    
    context = {
        'form': form,
        'title': 'Ajouter un modèle',
    }
    return render(request, 'modeles/modele_form.html', context)


def modele_update(request, pk):
    modele = get_object_or_404(Modele, pk=pk)
    
    if request.method == 'POST':
        form = ModeleForm(request.POST, request.FILES, instance=modele)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modèle modifié avec succès')
            return redirect('modeles:modele_detail', pk=modele.pk)
    else:
        form = ModeleForm(instance=modele)
    
    context = {
        'form': form,
        'modele': modele,
        'title': 'Modifier modèle',
    }
    return render(request, 'modeles/modele_form.html', context)


def modele_delete(request, pk):
    modele = get_object_or_404(Modele, pk=pk)
    modele.delete()
    messages.success(request, 'Modèle supprimé avec succès')
    return redirect('modeles:modele_list')
