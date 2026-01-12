from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from apps.personnel.models import Personnel
from .models import Message
from .forms import MessageForm

@login_required
def inbox(request):
    try:
        personnel_profile = request.user.personnel_profile
        received_messages = Message.objects.filter(recipient=personnel_profile)
    except Personnel.DoesNotExist:
        received_messages = []
        messages.info(request, "Pour recevoir des messages, votre compte utilisateur doit être lié à une fiche Personnel.")
    
    return render(request, 'messagerie/inbox.html', {
        'received_messages': received_messages,
        'active_tab': 'inbox'
    })

@login_required
def sent_messages(request):
    sent_messages = Message.objects.filter(sender=request.user)
    
    return render(request, 'messagerie/sent_messages.html', {
        'sent_messages': sent_messages,
        'active_tab': 'sent'
    })

@login_required
def compose(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, "Message envoyé avec succès !")
            return redirect('messagerie:inbox')
    else:
        form = MessageForm(user=request.user)
    
    return render(request, 'messagerie/compose.html', {
        'form': form,
    })

@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    
    # Vérifier que l'utilisateur est soit l'expéditeur, soit le destinataire
    is_sender = message.sender == request.user
    
    try:
        is_recipient = message.recipient == request.user.personnel_profile
    except Personnel.DoesNotExist:
        is_recipient = False

    if not (is_sender or is_recipient):
        messages.error(request, "Accès refusé.")
        return redirect('messagerie:inbox')
        
    if is_recipient and not message.is_read:
        message.is_read = True
        message.save()
    
    return render(request, 'messagerie/message_detail.html', {
        'message': message,
        'is_sender': is_sender
    })

@login_required
@require_http_methods(["POST"])
def mark_message_read(request, pk):
    try:
        message = get_object_or_404(Message, pk=pk)
        
        try:
            is_recipient = message.recipient == request.user.personnel_profile
        except Personnel.DoesNotExist:
            is_recipient = False
        
        if not is_recipient:
            return JsonResponse({'success': False, 'error': 'Accès refusé'}, status=403)
        
        message.is_read = True
        message.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
@require_http_methods(["POST"])
def archive_message(request, pk):
    try:
        message = get_object_or_404(Message, pk=pk)
        
        try:
            is_recipient = message.recipient == request.user.personnel_profile
        except Personnel.DoesNotExist:
            is_recipient = False
        
        is_sender = message.sender == request.user
        
        if not (is_recipient or is_sender):
            return JsonResponse({'success': False, 'error': 'Accès refusé'}, status=403)
        
        message.is_archived = True
        message.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
@require_http_methods(["POST"])
def delete_message(request, pk):
    try:
        message = get_object_or_404(Message, pk=pk)
        
        try:
            is_recipient = message.recipient == request.user.personnel_profile
        except Personnel.DoesNotExist:
            is_recipient = False
        
        is_sender = message.sender == request.user
        
        if not (is_recipient or is_sender):
            return JsonResponse({'success': False, 'error': 'Accès refusé'}, status=403)
        
        message_id = message.pk
        message.delete()
        
        return JsonResponse({'success': True, 'message_id': message_id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
