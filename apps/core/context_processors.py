from .models import Notification

def notifications_processor(request):
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        return {
            'notifications_count': unread_notifications.count(),
            'recent_notifications': unread_notifications[:5]
        }
    return {
        'notifications_count': 0,
        'recent_notifications': []
    }
