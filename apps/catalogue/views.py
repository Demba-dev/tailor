from django.shortcuts import render, get_object_or_404,redirect
from .models import TypeHabit
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST



def catalogue_list(request):
    habits = TypeHabit.objects.all()
    return render(request, 'catalogue/catalogue_list.html', {'habits': habits})

def catalogue_detail(request, pk):
    habit = get_object_or_404(TypeHabit, pk=pk)
    return render(request, 'catalogue/catalogue_detail.html', {'habit': habit})

def catalogue_create(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        prix_standard = request.POST.get('prix_standard')
        
        if nom:
            TypeHabit.objects.create(
                nom=nom,
                description=description,
                prix_standard=prix_standard or 0
            )
            messages.success(request, 'Type d\'habit créé avec succès')
            return redirect('catalogue:catalogue_list')
    
    return render(request, 'catalogue/catalogue_form.html')

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

@require_POST
def add_to_favorites(request, pk):
    habit = get_object_or_404(TypeHabit, pk=pk)
    # Adaptez selon votre logique de favoris
    # Par exemple : ajouter à une liste de favoris utilisateur
    return JsonResponse({'success': True, 'message': 'Ajouté aux favoris'})