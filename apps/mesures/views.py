from django.shortcuts import render, redirect, get_object_or_404
from .models import Mesure
from .forms import MesureForm
from django.contrib import messages

def mesure_list(request, client_id=None):
    if client_id:
        mesures = Mesure.objects.filter(client_id=client_id)
    else:
        mesures = Mesure.objects.all()
    return render(request, 'mesures/mesure_list.html', {'mesures': mesures})

def mesure_create(request, client_id=None):
    if request.method == 'POST':
        form = MesureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mesures:mesure_list')
    else:
        initial = {}
        if client_id:
            initial['client'] = client_id
        form = MesureForm(initial=initial)
    return render(request, 'mesures/mesure_form.html', {'form': form, 'title': 'Ajouter mesure'})

def mesure_detail(request, pk):
    mesure = get_object_or_404(Mesure, pk=pk)
    return render(request, 'mesures/mesure_detail.html', {'mesure': mesure})

def mesure_duplicate(request, pk):
    mesure = get_object_or_404(Mesure, pk=pk)
    mesure.pk = None
    mesure.save()
    messages.success(request, 'Mesure dupliquée avec succès')
    return redirect('mesures:mesure_list_client', client_id=mesure.client.pk)

def mesure_update(request, pk):
    mesure = get_object_or_404(Mesure, pk=pk)
    if request.method == 'POST':
        form = MesureForm(request.POST, instance=mesure)
        if form.is_valid():
            form.save()
            return redirect('mesures:mesure_list')
    else:
        form = MesureForm(instance=mesure)
    return render(request, 'mesures/mesure_form.html', {'form': form, 'title': 'Modifier mesure'})

def mesure_print(request, pk):
    mesure = get_object_or_404(Mesure, pk=pk)
    return render(request, 'mesures/mesure_print.html', {'mesure': mesure})

def mesure_import(request):
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']
        try:
            import csv
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            for row in reader:
                # Adaptez selon votre modèle Mesure
                pass
            
            messages.success(request, 'Mesures importées avec succès')
            return redirect('mesures:mesure_list')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'import : {str(e)}')
    
    return render(request, 'mesures/mesure_import.html')

def mesure_bulk_delete(request):
    if request.method == 'POST':
        ids = request.POST.getlist('mesure_ids')
        if ids:
            Mesure.objects.filter(pk__in=ids).delete()
            messages.success(request, f'{len(ids)} mesure(s) supprimée(s)')
        return redirect('mesures:mesure_list')
    return redirect('mesures:mesure_list')
def mesure_delete(request, pk):
    mesure = get_object_or_404(Mesure, pk=pk)
    mesure.delete()
    return redirect('mesures:mesure_list')
