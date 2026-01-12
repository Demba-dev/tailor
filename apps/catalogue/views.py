from django.shortcuts import render, get_object_or_404,redirect
from .models import TypeHabit
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import TypeHabitForm


@login_required
def catalogue_list(request):
    habits = TypeHabit.objects.all()
    return render(request, 'catalogue/catalogue_list.html', {'habits': habits})

@login_required
def catalogue_detail(request, pk):
    habit = get_object_or_404(TypeHabit, pk=pk)
    return render(request, 'catalogue/catalogue_detail.html', {'habit': habit})

@login_required
def catalogue_create(request):
    if request.method == 'POST':
        form = TypeHabitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Type d\'habit créé avec succès')
            return redirect('catalogue:catalogue_list')
    else:
        form = TypeHabitForm()
    
    return render(request, 'catalogue/catalogue_form.html', {'form': form, 'title': 'Créer un type d\'habit'})


@login_required
def catalogue_update(request, pk):
    habit = get_object_or_404(TypeHabit, pk=pk)
    if request.method == 'POST':
        form = TypeHabitForm(request.POST, request.FILES, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Type d\'habit modifié avec succès')
            return redirect('catalogue:catalogue_detail', pk=habit.pk)
    else:
        form = TypeHabitForm(instance=habit)
    
    return render(request, 'catalogue/catalogue_form.html', {'form': form, 'title': 'Modifier type d\'habit'})

@login_required
def catalogue_import(request):
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']
        try:
            import csv
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            for row in reader:
                # Adaptez selon votre modèle Catalogue
                pass
            
            messages.success(request, 'Données importées avec succès')
            return redirect('catalogue:catalogue_list')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'import : {str(e)}')
    
    return render(request, 'catalogue/catalogue_import.html')

@login_required
@require_POST
def add_to_favorites(request, pk):
    habit = get_object_or_404(TypeHabit, pk=pk)
    # Adaptez selon votre logique de favoris
    # Par exemple : ajouter à une liste de favoris utilisateur
    return JsonResponse({'success': True, 'message': 'Ajouté aux favoris'})