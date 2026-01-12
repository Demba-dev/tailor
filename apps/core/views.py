from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'core/notifications.html', {'notifications': notifications})

@login_required
def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    if notification.link:
        return redirect(notification.link)
    return redirect('core:notification_list')

@login_required
def mark_all_as_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', 'core:notification_list'))
