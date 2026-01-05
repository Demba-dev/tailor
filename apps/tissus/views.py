from django.shortcuts import render, get_object_or_404, redirect
from .models import Tissu
from django.contrib import messages


def tissu_list(request):
    tissus = Tissu.objects.filter(actif=True)
    matiere_filter = request.GET.get('matiere')
    motif_filter = request.GET.get('motif')
    search = request.GET.get('search')
    
    if matiere_filter:
        tissus = tissus.filter(matiere=matiere_filter)
    if motif_filter:
        tissus = tissus.filter(motif=motif_filter)
    if search:
        tissus = tissus.filter(nom__icontains=search)
    
    context = {
        'tissus': tissus,
        'matieres': Tissu.MATIERE_CHOICES,
        'motifs': Tissu.MOTIF_CHOICES,
    }
    return render(request, 'tissus/tissu_list.html', context)


def tissu_detail(request, pk):
    tissu = get_object_or_404(Tissu, pk=pk)
    context = {'tissu': tissu}
    return render(request, 'tissus/tissu_detail.html', context)


def tissu_create(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        matiere = request.POST.get('matiere')
        motif = request.POST.get('motif')
        couleur = request.POST.get('couleur')
        prix_metre = request.POST.get('prix_metre')
        stock_metres = request.POST.get('stock_metres')
        image = request.FILES.get('image')
        
        if nom and matiere and prix_metre:
            Tissu.objects.create(
                nom=nom,
                description=description,
                matiere=matiere,
                motif=motif,
                couleur=couleur,
                prix_metre=prix_metre,
                stock_metres=stock_metres or 0,
                image=image,
            )
            messages.success(request, 'Tissu ajouté avec succès')
            return redirect('tissus:tissu_list')
    
    context = {
        'matieres': Tissu.MATIERE_CHOICES,
        'motifs': Tissu.MOTIF_CHOICES,
    }
    return render(request, 'tissus/tissu_form.html', context)


def tissu_update(request, pk):
    tissu = get_object_or_404(Tissu, pk=pk)
    
    if request.method == 'POST':
        tissu.nom = request.POST.get('nom', tissu.nom)
        tissu.description = request.POST.get('description', tissu.description)
        tissu.matiere = request.POST.get('matiere', tissu.matiere)
        tissu.motif = request.POST.get('motif', tissu.motif)
        tissu.couleur = request.POST.get('couleur', tissu.couleur)
        tissu.prix_metre = request.POST.get('prix_metre', tissu.prix_metre)
        tissu.stock_metres = request.POST.get('stock_metres', tissu.stock_metres)
        
        if request.FILES.get('image'):
            tissu.image = request.FILES['image']
        
        tissu.save()
        messages.success(request, 'Tissu modifié avec succès')
        return redirect('tissus:tissu_detail', pk=tissu.pk)
    
    context = {
        'tissu': tissu,
        'matieres': Tissu.MATIERE_CHOICES,
        'motifs': Tissu.MOTIF_CHOICES,
    }
    return render(request, 'tissus/tissu_form.html', context)


def tissu_delete(request, pk):
    tissu = get_object_or_404(Tissu, pk=pk)
    tissu.delete()
    messages.success(request, 'Tissu supprimé avec succès')
    return redirect('tissus:tissu_list')
