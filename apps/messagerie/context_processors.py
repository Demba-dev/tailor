from .models import Message
from apps.personnel.models import Personnel

def unread_messages_count(request):
    if request.user.is_authenticated:
        try:
            personnel_profile = request.user.personnel_profile
            unread_count = Message.objects.filter(recipient=personnel_profile, is_read=False).count()
            recent_messages = Message.objects.filter(recipient=personnel_profile).order_by('-created_at')[:5]
            return {
                'unread_messages_count': unread_count,
                'recent_user_messages': recent_messages
            }
        except Personnel.DoesNotExist:
            pass
    return {
        'unread_messages_count': 0,
        'recent_user_messages': []
    }
