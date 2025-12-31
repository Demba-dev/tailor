from django.core.exceptions import PermissionDenied

def admin_required(user):
    """Autorise uniquement les administrateurs"""
    return user.is_authenticated and user.is_staff


def staff_required(user):
    """Autorise le personnel (admin + employés)"""
    return user.is_authenticated and user.is_staff


def owner_required(obj, user):
    """Vérifie que l'utilisateur est propriétaire de l'objet"""
    return obj.created_by == user
