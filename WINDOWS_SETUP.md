# Guide Installation Windows

## 📋 Prérequis

- Windows 10 / 11 (64-bit recommandé)
- 2GB RAM minimum
- 500MB espace disque

---

## 1️⃣ Installation de Python

### 1.1 Télécharger Python
1. Aller sur https://www.python.org/downloads/
2. Télécharger **Python 3.11 ou 3.13**
3. ⚠️ **IMPORTANT**: Cocher "Add Python to PATH" pendant l'installation

### 1.2 Vérifier l'Installation
Ouvrir **PowerShell** ou **Invite de Commande** et exécuter:
```powershell
python --version
# Résultat: Python 3.13.7 (ou version similaire)

pip --version
# Résultat: pip 24.x.x ...
```

---

## 2️⃣ Cloner le Projet

### 2.1 Créer le Dossier de Travail
```powershell
# Créer dossier
mkdir C:\Dev
cd C:\Dev

# Ou utiliser un autre chemin sans espaces
mkdir D:\Projects
cd D:\Projects
```

### 2.2 Cloner le Projet
```powershell
# Avec Git
git clone https://github.com/yourrepo/tailor.git
cd tailor

# Ou télécharger le ZIP et extraire
# puis:
cd C:\Dev\tailor
```

---

## 3️⃣ Créer l'Environnement Virtuel

### 3.1 Windows PowerShell
```powershell
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Résultat: (venv) C:\Dev\tailor>
```

### 3.2 Windows CMD (Invite de Commande)
```cmd
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
venv\Scripts\activate.bat

# Résultat: (venv) C:\Dev\tailor>
```

⚠️ **Si erreur d'activation sur PowerShell:**
```powershell
# Changer la politique d'exécution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Puis activer l'environnement
.\venv\Scripts\Activate.ps1
```

### 3.3 Vérifier l'Activation
```powershell
where python
# Résultat: C:\Dev\tailor\venv\Scripts\python.exe

python --version
```

---

## 4️⃣ Installer les Dépendances Python

### 4.1 Fichier requirements.txt
Vérifier que le fichier existe:
```powershell
dir requirements.txt
# Ou si dans venv activé:
ls requirements.txt
```

Si le fichier existe:
```powershell
pip install -r requirements.txt

# Résultat: Successfully installed django-4.2.x, ...
```

### 4.2 Si requirements.txt Manquant
Créer le fichier manuellement:
```powershell
pip install django==4.2
pip install psycopg2-binary
pip install pillow
pip install python-dateutil
pip install requests
pip install django-widget-tweaks

# Générer la liste pour plus tard:
pip freeze > requirements.txt
```

---

## 5️⃣ Configuration Django

### 5.1 Vérifier les Paramètres
```powershell
# Afficher la configuration
python manage.py shell
>>> from django.conf import settings
>>> print(f"DEBUG: {settings.DEBUG}")
>>> print(f"STATIC_URL: {settings.STATIC_URL}")
>>> exit()
```

### 5.2 Migrations de Base de Données
```powershell
# Créer les tables
python manage.py migrate

# Résultat: Running migrations...
#          OK
```

### 5.3 Créer un Superuser (Admin)
```powershell
python manage.py createsuperuser

# Entrer:
# Username: admin
# Email: admin@example.com
# Password: (votre mot de passe)
# Password (again): (confirmer)
```

### 5.4 Collecter les Ressources Statiques
```powershell
python manage.py collectstatic --noinput

# Résultat: 127 static files copied to '...\staticfiles'
```

---

## 6️⃣ Démarrer l'Application

### 6.1 Option 1: Script Windows

**Créer `run_dev.bat` dans le dossier projet:**
```batch
@echo off
set DJANGO_SETTINGS_MODULE=config.settings.development
python manage.py runserver 0.0.0.0:8000
pause
```

**Double-cliquer sur `run_dev.bat`** pour lancer

### 6.2 Option 2: PowerShell Directement
```powershell
# Vérifier que venv est activé
.\venv\Scripts\Activate.ps1

# Démarrer le serveur
python manage.py runserver

# Résultat:
# Watching for file changes with StatReloader
# Starting development server at http://127.0.0.1:8000/
```

### 6.3 Option 3: CMD (Invite de Commande)
```cmd
# Vérifier que venv est activé
venv\Scripts\activate.bat

# Démarrer le serveur
python manage.py runserver 0.0.0.0:8000

# Résultat: Starting development server...
```

---

## 7️⃣ Accéder à l'Application

### 7.1 Login
1. Ouvrir navigateur: **http://localhost:8000/users/login/**
2. Entrer identifiants du superuser créé
3. Cliquer "Connexion"

### 7.2 Admin Django
1. Aller à: **http://localhost:8000/admin/**
2. Identifiants superuser
3. Gérer les paramètres de l'application

### 7.3 Dashboard Principal
- **URL**: http://localhost:8000/dashboard/
- Vue principale après connexion

---

## ⚠️ Problèmes Courants Windows

### Problème 1: "python" non reconnu
**Solution:**
```powershell
# Vérifier installation Python
python --version

# Si erreur, réinstaller Python avec "Add Python to PATH"
# Ou utiliser le chemin complet:
C:\Users\Votre_Nom\AppData\Local\Programs\Python\Python313\python.exe --version
```

### Problème 2: Erreur d'activation venv sur PowerShell
**Solution:**
```powershell
# Exécuter en tant qu'admin et:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Ou utiliser CMD à la place:
venv\Scripts\activate.bat
```

### Problème 3: Port 8000 déjà utilisé
**Solution:**
```powershell
# Utiliser un autre port
python manage.py runserver 0.0.0.0:8080

# Ou trouver le processus qui l'utilise:
netstat -ano | findstr :8000

# Et le tuer:
taskkill /PID <PID> /F
```

### Problème 4: "Django secret key not found"
**Solution:**
Vérifier que le fichier `.env` existe à la racine:
```
SECRET_KEY=votre-clé-secrète
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Problème 5: Erreur de base de données SQLite
**Solution:**
```powershell
# Supprimer et recréer
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 📁 Structure Finale du Projet

```
C:\Dev\tailor\
├── venv\                    # Environnement virtuel
├── config\                  # Configuration Django
│   ├── settings\
│   │   ├── base.py         # Paramètres principaux
│   │   └── development.py  # Paramètres dev
│   ├── urls.py
│   └── wsgi.py
├── apps\                    # Applications Django
├── templates\              # Templates HTML
├── static\                 # Ressources statiques (CSS, JS, Fonts)
│   └── vendor\            # Dépendances locales
├── staticfiles\           # Fichiers collectés
├── manage.py
├── db.sqlite3             # Base de données
├── requirements.txt       # Dépendances Python
├── run_dev.bat           # Script de démarrage (Windows)
├── OFFLINE_MODE.md       # Documentation offline
├── PROCEDURES_OFFLINE.md # Procédures de setup
└── WINDOWS_SETUP.md      # Ce fichier
```

---

## 🔄 Workflow Quotidien Windows

### Matin : Démarrer l'Application
```powershell
# Option 1: Double-cliquer sur run_dev.bat

# Option 2: Manuel
cd C:\Dev\tailor
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

### Pendant le Développement
```powershell
# Django recharge automatiquement
# Ouvrir http://localhost:8000

# Modifier les fichiers .py ou .html
# L'app se recharge toute seule ✓

# Pour les migrations après modification de modèles:
python manage.py makemigrations
python manage.py migrate
```

### Arret : Arrêter l'Application
```powershell
# Dans le terminal de l'app:
Ctrl + C

# Désactiver venv (optionnel):
deactivate
```

---

## 📦 Commandes Essentielles Windows

```powershell
# Activer environnement
.\venv\Scripts\Activate.ps1

# Installer dépendances
pip install -r requirements.txt

# Créer superuser
python manage.py createsuperuser

# Migrer la base de données
python manage.py migrate

# Collecter les statiques
python manage.py collectstatic --noinput

# Démarrer l'app
python manage.py runserver

# Entrer dans la console Django
python manage.py shell

# Créer nouvelle app
python manage.py startapp nom_app

# Faire migrations
python manage.py makemigrations

# Appliquer migrations
python manage.py migrate

# Désactiver venv
deactivate
```

---

## ✅ Vérification Installation Réussie

```powershell
# 1. Vérifier Python
python --version
# ✓ Python 3.13.x

# 2. Vérifier venv activé
where python
# ✓ C:\Dev\tailor\venv\Scripts\python.exe

# 3. Vérifier Django
python -m django --version
# ✓ 4.2.x

# 4. Vérifier base de données
ls db.sqlite3
# ✓ db.sqlite3

# 5. Vérifier statiques
ls staticfiles
# ✓ statiques collectés

# 6. Démarrer l'app
python manage.py runserver
# ✓ Starting development server at http://127.0.0.1:8000/
```

---

## 🌐 Accès Depuis Autre Machine

Pour accéder à l'app depuis une autre machine sur le même réseau:

```powershell
# Démarrer avec l'IP locale
python manage.py runserver 0.0.0.0:8000

# Trouver votre IP
ipconfig

# Résultat: IPv4 Address: 192.168.1.100

# Accéder depuis autre machine:
# http://192.168.1.100:8000/
```

---

## 📝 Notes Importantes Windows

1. **Chemins**: Utiliser `/` ou `\` (Django gère les deux)
2. **Encodage**: Windows CMD peut avoir des problèmes UTF-8
   - Solution: `chcp 65001` en CMD
3. **Permissions**: Si erreur permissions, exécuter PowerShell en admin
4. **Antivirus**: Peut bloquer les ports
   - Ajouter Python à la whitelist
5. **Espaces dans chemins**: Éviter
   - ❌ `C:\Mes Documents\tailor`
   - ✓ `C:\Dev\tailor`

---

## 🚀 Prêt?

Vous êtes maintenant prêt à utiliser le projet sur Windows!

1. ✅ Python installé
2. ✅ Environnement virtuel créé
3. ✅ Dépendances installées
4. ✅ Base de données migrée
5. ✅ Statiques collectés
6. ✅ App en cours d'exécution

**Accédez à**: http://localhost:8000/users/login/
