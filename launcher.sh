#!/bin/bash

# Chemin vers le dossier du projet
PROJECT_DIR="/home/demba/dev/django/tailor"
cd "$PROJECT_DIR"

# Activation de l'environnement virtuel
source venv/bin/activate

# Libérer le port 8000 s'il est déjà utilisé
fuser -k 8000/tcp 2>/dev/null

# Ouvrir Chrome en mode "App" (fenêtre seule sans interface de navigation)
(sleep 2 && google-chrome --app=http://127.0.0.1:8000) &

# Lancement du serveur Django
python manage.py runserver
