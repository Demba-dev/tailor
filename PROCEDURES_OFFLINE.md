# Procédures : Rendre le Projet Local (Offline)

## 📋 Table des Matières
1. [Analyse Initiale](#analyse-initiale)
2. [Étape 1 : Audit des Dépendances CDN](#étape-1--audit-des-dépendances-cdn)
3. [Étape 2 : Organisation des Ressources Statiques](#étape-2--organisation-des-ressources-statiques)
4. [Étape 3 : Configuration Django](#étape-3--configuration-django)
5. [Étape 4 : Remplacement des CDN dans les Templates](#étape-4--remplacement-des-cdn-dans-les-templates)
6. [Étape 5 : Collecte des Ressources Statiques](#étape-5--collecte-des-ressources-statiques)
7. [Étape 6 : Test et Vérification](#étape-6--test-et-vérification)
8. [Résumé des Fichiers Modifiés](#résumé-des-fichiers-modifiés)

---

## Analyse Initiale

### Problèmes Identifiés
- ❌ Application dépendante d'Internet pour charger CSS, JS, Fonts
- ❌ CDN multiples utilisés: `jsdelivr.net`, `cdnjs.cloudflare.com`, `fonts.googleapis.com`, `code.jquery.com`
- ❌ Design cassé sans connexion (logo invisible, CSS non chargé)
- ❌ Fonts Google non disponibles localement

### Ressources Existantes
- ✓ Dossier `/static/vendor/` avec 127 fichiers statiques déjà présents
- ✓ Webfonts Font Awesome déjà téléchargés
- ✓ Bootstrap, jQuery, Chart.js, DataTables localement disponibles

---

## Étape 1 : Audit des Dépendances CDN

### Commande : Identifier tous les CDN
```bash
# Chercher toutes les références CDN dans les templates
grep -r "https://cdn\|https://fonts\|https://code.jquery\|https://cdnjs" \
  /path/to/project/templates --include="*.html"

grep -r "https://cdn\|https://fonts\|https://code.jquery\|https://cdnjs" \
  /path/to/project/apps --include="*.html"
```

### CDN Trouvés
| CDN | Usage | Fichier Local |
|-----|-------|---------------|
| `https://fonts.googleapis.com` | Google Fonts | `/static/vendor/fonts/fonts.css` |
| `https://cdn.jsdelivr.net/npm/bootstrap@5.3.2` | Bootstrap CSS/JS | `/static/vendor/bootstrap/` |
| `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0` | Font Awesome | `/static/vendor/fontawesome/` |
| `https://cdn.jsdelivr.net/npm/chart.js` | Chart.js | `/static/vendor/chartjs/` |
| `https://cdn.datatables.net` | DataTables | `/static/vendor/datatables/` |
| `https://cdnjs.cloudflare.com/animate.css` | Animate.css | `/static/vendor/animate/` |
| `https://code.jquery.com/jquery-3.7.0` | jQuery | `/static/vendor/jquery/` |
| `https://cdn.jsdelivr.net/npm/toastr` | Toastr | `/static/vendor/toastr/` |

---

## Étape 2 : Organisation des Ressources Statiques

### Vérifier la Structure Existante
```bash
# Vérifier que les dossiers vendor existent
ls -la /path/to/project/static/vendor/

# Résultat attendu:
# ✓ bootstrap/
# ✓ fontawesome/
# ✓ jquery/
# ✓ chartjs/
# ✓ datatables/
# ✓ animate/
# ✓ toastr/
# ✓ fonts/
```

### Vérifier les Webfonts Font Awesome
```bash
ls -la /static/vendor/fontawesome/webfonts/
# Doit contenir:
# ✓ fa-brands-400.woff2
# ✓ fa-regular-400.woff2
# ✓ fa-solid-900.woff2
```

---

## Étape 3 : Configuration Django

### 3.1 Modifier `config/settings/base.py`

**Ajouter après `STATIC_ROOT`:**
```python
# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ← AJOUTER CES LIGNES:
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

**Raison:** Django doit chercher les fichiers statiques dans le dossier `/static/` en plus de `staticfiles/`

### 3.2 Vérifier la Configuration
```bash
python manage.py shell << 'EOF'
from django.conf import settings
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
print(f"DEBUG: {settings.DEBUG}")
EOF
```

---

## Étape 4 : Remplacement des CDN dans les Templates

### 4.1 Template Principal (`templates/base.html`)

**Avant:**
```html
<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">

<!-- Bootstrap 5 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Font Awesome 6 -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
```

**Après:**
```html
{% load static %}

<!-- Google Fonts (Local) -->
<link rel="stylesheet" href="{% static 'vendor/fonts/fonts.css' %}">

<!-- Bootstrap 5 (Local) -->
<link href="{% static 'vendor/bootstrap/css/bootstrap.min.css' %}" rel="stylesheet">

<!-- Font Awesome 6 (Local) -->
<link rel="stylesheet" href="{% static 'vendor/fontawesome/css/all.min.css' %}">
```

### 4.2 Remplacer les JS
**Avant:**
```html
<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
```

**Après:**
```html
<script src="{% static 'vendor/jquery/jquery-3.7.0.min.js' %}"></script>
<script src="{% static 'vendor/bootstrap/js/bootstrap.bundle.min.js' %}"></script>
<script src="{% static 'vendor/datatables/js/jquery.dataTables.min.js' %}"></script>
<script src="{% static 'vendor/datatables/js/dataTables.bootstrap5.min.js' %}"></script>
```

### 4.3 Script Automatisé (Python)

```python
import os
import re
from pathlib import Path

dirs_to_process = [
    '/path/to/project/apps',
    '/path/to/project/templates',
]

replacements = [
    # Google Fonts
    (r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?<link href="https://fonts\.googleapis\.com/[^"]*" rel="stylesheet">',
     '<link rel="stylesheet" href="{% static \'vendor/fonts/fonts.css\' %}">'),
    
    # Bootstrap CSS
    (r'<link href="https://cdn\.jsdelivr\.net/npm/bootstrap@[^"]*\.css" rel="stylesheet">',
     '<link href="{% static \'vendor/bootstrap/css/bootstrap.min.css\' %}" rel="stylesheet">'),
    
    # Font Awesome
    (r'<link rel="stylesheet" href="https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]*\.css">',
     '<link rel="stylesheet" href="{% static \'vendor/fontawesome/css/all.min.css\' %}">'),
    
    # Animate.css
    (r'<link rel="stylesheet" href="https://cdnjs\.cloudflare\.com/ajax/libs/animate\.css/[^"]*\.css">',
     '<link rel="stylesheet" href="{% static \'vendor/animate/animate.min.css\' %}">'),
    
    # jQuery
    (r'<script src="https://code\.jquery\.com/jquery-[^"]*\.js"></script>',
     '<script src="{% static \'vendor/jquery/jquery-3.7.0.min.js\' %}"></script>'),
    
    # Bootstrap JS
    (r'<script src="https://cdn\.jsdelivr\.net/npm/bootstrap@[^"]*\.js"></script>',
     '<script src="{% static \'vendor/bootstrap/js/bootstrap.bundle.min.js\' %}"></script>'),
]

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Modifié: {filepath}")
        return True
    return False

# Traiter tous les fichiers HTML
for base_dir in dirs_to_process:
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                process_file(os.path.join(root, file))
```

### 4.4 Templates Modifiés
- `templates/base.html` - Template principal
- `templates/404.html` - Page erreur
- `apps/users/templates/users/user_login.html` - Connexion
- **12+ autres templates** d'applications

---

## Étape 5 : Collecte des Ressources Statiques

### 5.1 Collecter les Fichiers Statiques
```bash
cd /path/to/project

# Option 1: Collecter avec suppression des anciens
python manage.py collectstatic --noinput --clear

# Résultat:
# 127 static files copied to '/path/to/project/staticfiles'
```

### 5.2 Vérifier la Collecte
```bash
ls -la /path/to/project/staticfiles/vendor/

# Doit contenir:
# ✓ bootstrap/
# ✓ fontawesome/
# ✓ jquery/
# ✓ chartjs/
# ✓ datatables/
# ✓ animate/
# ✓ toastr/
# ✓ fonts/
```

---

## Étape 6 : Test et Vérification

### 6.1 Créer le Script de Démarrage

**Fichier: `run_dev.sh`**
```bash
#!/bin/bash
export DJANGO_SETTINGS_MODULE=config.settings.development
python manage.py runserver 0.0.0.0:8000
```

Rendre exécutable:
```bash
chmod +x run_dev.sh
```

### 6.2 Démarrer l'Application
```bash
./run_dev.sh

# Ou manuellement:
python manage.py runserver
```

### 6.3 Tests d'Accès aux Ressources Statiques

```bash
# Test 1: Bootstrap CSS
curl -I "http://localhost:8000/static/vendor/bootstrap/css/bootstrap.min.css"
# Résultat: HTTP/1.1 200 OK

# Test 2: Font Awesome CSS
curl -I "http://localhost:8000/static/vendor/fontawesome/css/all.min.css"
# Résultat: HTTP/1.1 200 OK

# Test 3: jQuery
curl -I "http://localhost:8000/static/vendor/jquery/jquery-3.7.0.min.js"
# Résultat: HTTP/1.1 200 OK

# Test 4: Fonts
curl -I "http://localhost:8000/static/vendor/fonts/fonts.css"
# Résultat: HTTP/1.1 200 OK
```

### 6.4 Vérifier l'Absence de CDN

```bash
# Vérifier qu'aucun CDN n'est utilisé
curl -s "http://localhost:8000/users/login/" | grep -E "https://cdn|https://fonts.googleapis|https://code.jquery|https://cdnjs"

# Résultat attendu: (aucun résultat = succès ✓)
```

### 6.5 Vérifier les Ressources Locales

```bash
# Compter les ressources locales
curl -s "http://localhost:8000/users/login/" | grep -c "/static/vendor"

# Résultat: 4+ (nombre de ressources locales)
```

### 6.6 Test Complet (Script)

```bash
echo "=== TEST OFFLINE ==="
echo ""
echo "1. Ressources statiques accessibles:"
curl -I "http://localhost:8000/static/vendor/bootstrap/css/bootstrap.min.css" | grep HTTP
curl -I "http://localhost:8000/static/vendor/fontawesome/css/all.min.css" | grep HTTP
curl -I "http://localhost:8000/static/vendor/fonts/fonts.css" | grep HTTP
echo ""
echo "2. Pas de CDN détectés:"
if curl -s "http://localhost:8000/users/login/" | grep -q "https://cdn\|https://fonts.googleapis"; then
  echo "✗ ERREUR: CDN trouvés"
else
  echo "✓ Aucun CDN - Application offline OK"
fi
```

---

## Résumé des Fichiers Modifiés

| Fichier | Type | Modification |
|---------|------|--------------|
| `config/settings/base.py` | Configuration | Ajout `STATICFILES_DIRS` |
| `templates/base.html` | Template | Remplacement 8 CDN → versions locales |
| `templates/404.html` | Template | Remplacement 3 CDN → versions locales |
| `apps/users/templates/users/user_login.html` | Template | Remplacement 4 CDN → versions locales |
| `apps/*/templates/**/*.html` | Templates | Remplacement CDN (12+ fichiers) |
| `run_dev.sh` | Script | Nouveau script de démarrage |
| `OFFLINE_MODE.md` | Documentation | Docs mode offline |

### Fichiers **Non Modifiés** (statiques)
- `/static/vendor/*` - Déjà en place ✓
- `/staticfiles/*` - Généré automatiquement ✓
- Webfonts Font Awesome - Déjà présentes ✓

---

## Checklist de Validation

- [x] Tous les CDN identifiés et documentés
- [x] Ressources statiques organisées localement
- [x] Django configuré pour servir les fichiers statiques
- [x] Templates modifiés (base + applicatifs)
- [x] Collecte des ressources statiques réussie
- [x] Tests d'accès aux fichiers statiques (HTTP 200)
- [x] Vérification d'absence de CDN
- [x] Application fonctionnelle sans internet ✓

---

## Commandes Rapides de Référence

### Redémarrer l'Application
```bash
pkill -f "manage.py runserver"
sleep 2
./run_dev.sh
```

### Recollecte les Ressources
```bash
python manage.py collectstatic --noinput --clear
```

### Vérifier les Paramètres Statiques
```bash
python manage.py shell << 'EOF'
from django.conf import settings
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
EOF
```

### Nettoyer les Caches
```bash
# Vider les fichiers temporaires
rm -rf /tmp/django*

# Redémarrer
./run_dev.sh
```

---

## Résultat Final

✅ **Application complètement offline et fonctionnelle**

- 127 fichiers statiques collectés
- 0 dépendance CDN externe
- Chargement instantané sans latence réseau
- Design et CSS préservés
- Fonts Google servies localement
- Compatible 100% mode hors ligne
