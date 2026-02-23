# 🖥️ Intégration Desktop Linux

Ce guide explique comment installer TAILOR en tant qu'application Desktop native sur Linux.

---

## 📋 Fichiers Impliqués

### 1. **launcher.sh** - Script de Démarrage
C'est le **point d'entrée** de l'application:
- ✅ Vérifie l'environnement (Python, Django, venv)
- ✅ Affiche des messages colorés avec statuts
- ✅ Gère le port 8000 (libère s'il est occupé)
- ✅ Détecte et ouvre le navigateur (Chrome, Chromium, Firefox)
- ✅ Lance le serveur Django

### 2. **tailor.desktop** - Fichier Raccourci Desktop
C'est le **fichier de configuration** pour intégrer l'app au desktop:
- ✅ Enregistre l'app dans le menu Applications
- ✅ Ajoute une icone
- ✅ Ajoute des actions (Connexion, Admin, Dashboard)
- ✅ Configure les propriétés de l'app

---

## 🚀 Installation (Linux)

### Étape 1: Rendre launcher.sh Exécutable

```bash
cd /home/demba/dev/django/tailor
chmod +x launcher.sh
ls -la launcher.sh
# Résultat: -rwxr-xr-x ... launcher.sh ✓
```

### Étape 2: Vérifier l'Icone

```bash
ls -la /home/demba/dev/django/tailor/static/img/icons/tailor.jpg

# Si le fichier n'existe pas, utiliser une alternative:
# - /static/img/logo/favicon.ico
# - /static/img/logo/apple-touch-icon.png
```

### Étape 3: Installer le Fichier Desktop (optionnel)

#### Option A: Installation pour l'utilisateur seul
```bash
# Créer le dossier applications (s'il n'existe pas)
mkdir -p ~/.local/share/applications

# Copier le fichier desktop
cp /home/demba/dev/django/tailor/tailor.desktop ~/.local/share/applications/

# Mettre à jour la base de données desktop
update-desktop-database ~/.local/share/applications
```

#### Option B: Installation système (admin)
```bash
# Copier pour tous les utilisateurs
sudo cp /home/demba/dev/django/tailor/tailor.desktop /usr/share/applications/

# Mettre à jour la base
sudo update-desktop-database /usr/share/applications
```

### Étape 4: Vérifier l'Installation

```bash
# Vérifier que le fichier est installé
ls ~/.local/share/applications/tailor.desktop

# Vérifier la validité
desktop-file-validate ~/.local/share/applications/tailor.desktop
# Résultat: (pas d'erreur = OK ✓)
```

---

## 🎯 Utilisation

### Méthode 1: Via le Menu Applications
1. Ouvrir le menu "Affichages" ou "Applications"
2. Chercher "TAILOR" ou "Atelier de Couture"
3. Cliquer pour lancer

### Méthode 2: Via Ligne de Commande
```bash
# Lancer via le fichier desktop
gtk-launch tailor

# Ou directement le script
/home/demba/dev/django/tailor/launcher.sh
```

### Méthode 3: Via Spotlight (Ubuntu)
1. Appuyer sur `Super` (touche Windows)
2. Taper "TAILOR"
3. Appuyer sur Entrée

### Méthode 4: Actions Rapides (Clic Droit)
Après installation du fichier .desktop:
1. Ouvrir le gestionnaire de fichiers
2. Chercher l'app dans les applications
3. Clic droit → Actions disponibles:
   - **Connexion** - Lance l'app
   - **Administration** - Ouvre http://127.0.0.1:8000/admin/
   - **Tableau de Bord** - Ouvre http://127.0.0.1:8000/dashboard/

---

## 📊 Contenu de launcher.sh

### Vérifications Effectuées

```bash
┌─ Vérification du Dossier Projet
├─ Vérification de l'Environnement Virtuel
├─ Activation du venv
├─ Vérification de Django
├─ Libération du Port 8000
├─ Détection du Navigateur
└─ Démarrage du Serveur Django
```

### Messages d'Erreur Gérés

| Erreur | Message | Correction |
|--------|---------|-----------|
| Dossier manquant | "Le dossier du projet n'existe pas" | Vérifier le chemin |
| venv manquant | "Environnement virtuel non trouvé" | `python3 -m venv venv` |
| Django manquant | "Django n'est pas installé" | `pip install -r requirements.txt` |
| Port occupé | "Le port 8000 est déjà utilisé" | Script libère le port auto |
| Navigateur manquant | "Aucun navigateur détecté" | Ouvrir manuellement |

### Sorties Colorées

Le script utilise des couleurs pour faciliter la lecture:
- 🔴 **Rouge** = Erreur critique
- 🟢 **Vert** = Succès/OK
- 🟡 **Jaune** = Avertissement
- 🔵 **Bleu** = Information

Exemple:
```
╔═══════════════════════════════════════════════════════╗
║     TAILOR - Gestion d'Atelier de Couture            ║
║          Démarrage de l'Application                   ║
╚═══════════════════════════════════════════════════════╝

✓ Dossier du projet trouvé
✓ Environnement virtuel trouvé
→ Activation de l'environnement virtuel...
✓ Django est prêt
⚠ Le port 8000 est déjà utilisé, libération...

╔═══════════════════════════════════════════════════════╗
✓ Tous les contrôles sont passés
╚═══════════════════════════════════════════════════════╝

Accédez à l'application:
  - Login: http://127.0.0.1:8000/users/login/
  - Admin: http://127.0.0.1:8000/admin/
  - Dashboard: http://127.0.0.1:8000/dashboard/

Pour arrêter: Ctrl + C
```

---

## 📋 Contenu de tailor.desktop

### Sections

```ini
[Desktop Entry]
# Section principale avec infos de base

[Desktop Action OpenLogin]
# Action 1: Ouvrir la connexion

[Desktop Action OpenAdmin]
# Action 2: Ouvrir l'admin

[Desktop Action OpenDashboard]
# Action 3: Ouvrir le dashboard
```

### Propriétés Principales

| Propriété | Valeur | Explication |
|-----------|--------|-------------|
| **Name** | TAILOR - Atelier de Couture | Nom affiché dans le menu |
| **Comment** | Système de gestion d'atelier... | Description courte |
| **Icon** | /static/img/icons/tailor.jpg | Icone affichée |
| **Exec** | launcher.sh | Script à exécuter |
| **Type** | Application | Type d'entrée |
| **Terminal** | false | Ne pas afficher terminal |
| **Categories** | Development;Utility;Business | Catégories du menu |

---

## 🔧 Personnalisation

### Changer l'Icone

**Éditer**: `tailor.desktop`
```ini
# Avant:
Icon=/home/demba/dev/django/tailor/static/img/icons/tailor.jpg

# Après (exemple):
Icon=/usr/share/icons/hicolor/256x256/apps/tailor.png
# Ou utiliser un nom d'icone système:
Icon=document-properties
```

### Changer la Catégorie

```ini
# Avant:
Categories=Development;Utility;Business;

# Après (pour Éducation):
Categories=Education;

# Catégories disponibles:
# - Utility: Utilitaires
# - Development: Développement  
# - Office: Bureau
# - Business: Affaires
# - Education: Éducation
```

### Ajouter une Nouvelle Action

**Éditer**: `tailor.desktop`

```ini
# Dans Actions:
Actions=OpenLogin;OpenAdmin;OpenDashboard;OpenCustom;

# Ajouter une nouvelle section:
[Desktop Action OpenCustom]
Name=Ma Nouvelle Action
Exec=bash -c "echo 'Action custom' && firefox"
```

### Changer le Chemin du Projet

Si le projet est dans un autre dossier:

**launcher.sh**:
```bash
# Ligne 9:
PROJECT_DIR="/path/to/your/project"
```

**tailor.desktop**:
```ini
Exec=/path/to/your/project/launcher.sh
Path=/path/to/your/project
```

---

## 🐛 Dépannage

### Problème: L'app n'apparaît pas dans le menu
**Solution:**
```bash
# Réinstaller le fichier desktop
cp tailor.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications

# Ou utiliser la commande de validation
desktop-file-validate ~/.local/share/applications/tailor.desktop
```

### Problème: Icone non visible
**Solution:**
1. Vérifier que le chemin de l'icone existe
2. Changer en icone système:
   ```ini
   Icon=application-x-executable
   ```
3. Vider le cache:
   ```bash
   rm -rf ~/.cache/icon-cache
   ```

### Problème: Script ne s'exécute pas
**Solution:**
```bash
# Rendre le script exécutable
chmod +x launcher.sh

# Vérifier les permissions
ls -la launcher.sh
# Doit avoir: -rwxr-xr-x
```

### Problème: Erreur "Not a valid application"
**Solution:**
```bash
# Valider le fichier
desktop-file-validate tailor.desktop

# Corriger les erreurs affichées
# Puis réinstaller
```

---

## 📱 Pour Windows et macOS

Utiliser plutôt:
- **Windows**: `run_dev.bat` (double-cliquer)
- **macOS**: Créer un `.app` ou utiliser `./run_dev.sh`

---

## ✅ Vérification Finale

Après installation:

```bash
# 1. Vérifier les fichiers
ls -la launcher.sh tailor.desktop

# 2. Tester le script directement
./launcher.sh

# 3. Vérifier l'installation desktop
ls ~/.local/share/applications/tailor.desktop

# 4. Valider le format
desktop-file-validate ~/.local/share/applications/tailor.desktop

# 5. Rechercher l'app dans le menu
gtk-launch tailor
```

---

## 🎯 Prochain Démarrage

Après installation, simplement:
1. **Cliquer** sur "TAILOR" dans le menu Applications
2. **Attendre** l'ouverture du navigateur (2-3 secondes)
3. **Vous êtes connecté!** ✅

---

## 📝 Notes

- Le script `launcher.sh` est **robuste** et gère les erreurs
- Le fichier `tailor.desktop` suit les **standards freedesktop.org**
- L'application s'ouvre dans une **fenêtre navigateur** (pas de chrome browser)
- Le serveur Django continue de **tourner en arrière-plan**
- Pour arrêter: **Ctrl + C** dans le terminal du serveur

Vous êtes maintenant prêt à utiliser TAILOR comme une **application desktop native!** 🎉
