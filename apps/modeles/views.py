from django.shortcuts import render, get_object_or_404, redirect
from .models import Modele
from django.contrib import messages


def modele_list(request):
    modeles = Modele.objects.filter(actif=True)
    type_filter = request.GET.get('type')
    difficulte_filter = request.GET.get('difficulte')
    search = request.GET.get('search')
    
    if type_filter:
        modeles = modeles.filter(type_habit=type_filter)
    if difficulte_filter:
        modeles = modeles.filter(difficulte=difficulte_filter)
    if search:
        modeles = modeles.filter(nom__icontains=search)
    
    context = {
        'modeles': modeles,
        'difficultes': Modele.DIFFICULTE_CHOICES,
    }
    return render(request, 'modeles/modele_list.html', context)


def modele_detail(request, pk):
    modele = get_object_or_404(Modele, pk=pk)
    context = {'modele': modele}
    return render(request, 'modeles/modele_detail.html', context)


def modele_create(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        difficulte = request.POST.get('difficulte')
        type_habit = request.POST.get('type_habit')
        temps_realisation_heures = request.POST.get('temps_realisation_heures')
        prix_main_oeuvre = request.POST.get('prix_main_oeuvre')
        description_technique = request.POST.get('description_technique')
        image = request.FILES.get('image')
        
        if nom and type_habit and prix_main_oeuvre:
            Modele.objects.create(
                nom=nom,
                description=description,
                difficulte=difficulte or 'moyen',
                type_habit=type_habit,
                temps_realisation_heures=temps_realisation_heures or 4,
                prix_main_oeuvre=prix_main_oeuvre,
                description_technique=description_technique,
                image=image,
            )
            messages.success(request, 'Modèle ajouté avec succès')
            return redirect('modeles:modele_list')
    
    context = {
        'difficultes': Modele.DIFFICULTE_CHOICES,
    }
    return render(request, 'modeles/modele_form.html', context)


def modele_update(request, pk):
    modele = get_object_or_404(Modele, pk=pk)
    
    if request.method == 'POST':
        modele.nom = request.POST.get('nom', modele.nom)
        modele.description = request.POST.get('description', modele.description)
        modele.difficulte = request.POST.get('difficulte', modele.difficulte)
        modele.type_habit = request.POST.get('type_habit', modele.type_habit)
        modele.temps_realisation_heures = request.POST.get('temps_realisation_heures', modele.temps_realisation_heures)
        modele.prix_main_oeuvre = request.POST.get('prix_main_oeuvre', modele.prix_main_oeuvre)
        modele.description_technique = request.POST.get('description_technique', modele.description_technique)
        
        if request.FILES.get('image'):
            modele.image = request.FILES['image']
        
        modele.save()
        messages.success(request, 'Modèle modifié avec succès')
        return redirect('modeles:modele_detail', pk=modele.pk)
    
    context = {
        'modele': modele,
        'difficultes': Modele.DIFFICULTE_CHOICES,
    }
    return render(request, 'modeles/modele_form.html', context)


def modele_delete(request, pk):
    modele = get_object_or_404(Modele, pk=pk)
    modele.delete()
    messages.success(request, 'Modèle supprimé avec succès')
    return redirect('modeles:modele_list')
