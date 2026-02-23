from .base import *  # importe toutes les configurations de base

DEBUG = True        # active le mode développement

# Permettre tous les hosts en développement
ALLOWED_HOSTS = [
    '*',
    'localhost',
    '127.0.0.1',
    'tailor.local',
    'tailor.local:8000',
    '0.0.0.0',
]