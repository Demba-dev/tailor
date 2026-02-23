# 🏗️ Architecture du Projet

## 📁 Structure Complète

```
tailor/
├── config/                          # Configuration Django
│   ├── settings/
│   │   ├── base.py                 # Paramètres communs
│   │   ├── development.py          # Mode développement
│   │   └── production.py           # Mode production
│   ├── urls.py                     # URLs principales
│   └── wsgi.py                     # Configuration WSGI
│
├── apps/                            # Applications Django
│   ├── clients/                    # Gestion clients
│   ├── commandes/                  # Gestion commandes
│   ├── paiements/                  # Gestion paiements
│   ├── personnel/                  # Artisans/Personnel
│   ├── formations/                 # Formations
│   ├── catalogue/                  # Catalogue produits
│   ├── ventes/                     # Historique ventes
│   ├── mesures/                    # Mesures clients
│   ├── dashboard/                  # Tableau de bord
│   ├── users/                      # Authentification
│   ├── settings/                   # Paramètres application
│   └── messagerie/                 # Messagerie interne
│
├── templates/                       # Templates HTML globaux
│   ├── base.html                   # Template principal
│   ├── 404.html                    # Erreur 404
│   └── includes/
│       ├── sidebar.html            # Barre latérale
│       ├── navbar.html             # Barre navigation
│       └── footer.html             # Footer
│
├── static/                          # Fichiers statiques NON collectés
│   ├── css/
│   │   ├── tailor.css             # Styles personnalisés
│   │   ├── sidebar.css            # Styles sidebar
│   │   ├── responsive.css         # Design responsive
│   │   └── clients.css            # Styles clients
│   ├── js/
│   │   └── tailor.js              # ← JavaScript principal
│   ├── img/                        # Images du projet
│   └── vendor/                     # ← Dépendances externes
│       ├── bootstrap/              # Framework Bootstrap
│       ├── fontawesome/            # Icones Font Awesome
│       ├── jquery/                 # Bibliothèque jQuery
│       ├── chartjs/                # Graphiques Chart.js
│       ├── datatables/             # Tables DataTables
│       ├── animate/                # Animations Animate.css
│       ├── toastr/                 # Notifications Toastr
│       ├── fonts/                  # Fonts Google (local)
│       ├── flatpickr/              # Date picker Flatpickr
│       ├── cleavejs/               # Formatage inputs
│       ├── qrcode/                 # Génération QR codes
│       └── ...                     # Autres bibliothèques
│
├── staticfiles/                     # Fichiers collectés (généré)
│   └── (même structure que static/)
│
├── media/                           # Uploads utilisateurs
│   ├── logos/
│   ├── avatars/
│   └── documents/
│
├── db.sqlite3                       # Base de données locale
├── manage.py                        # Script Django
├── requirements.txt                 # Dépendances Python
├── OFFLINE_MODE.md                 # Documentation offline
├── WINDOWS_SETUP.md                # Installation Windows
└── ...
```

---

## 🎯 tailor.js - JavaScript Principal

### Qu'est-ce que c'est?
**`static/js/tailor.js`** est le **fichier JavaScript personnalisé** du projet qui contient:

### Contenu Détaillé

```javascript
// 1️⃣ INITIALISATION GLOBALE (DOMContentLoaded)
document.addEventListener('DOMContentLoaded', function() {
    // Exécuté quand le DOM est chargé
});

// 2️⃣ TOOLTIPS BOOTSTRAP
// Activation des infobulle au survol
const tooltipTriggerList = [...document.querySelectorAll('[data-bs-toggle="tooltip"]')];
const tooltipList = tooltipTriggerList.map(el => new bootstrap.Tooltip(el));

// 3️⃣ POPOVERS BOOTSTRAP
// Activation des popovers (infobulle avec contenu)
const popoverTriggerList = [...document.querySelectorAll('[data-bs-toggle="popover"]')];
const popoverList = popoverTriggerList.map(el => new bootstrap.Popover(el));

// 4️⃣ MESSAGES AUTO-FERMETURE
// Les alertes se ferment automatiquement après 5 secondes
const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
alerts.forEach(alert => {
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    }, 5000);
});

// 5️⃣ FONCTION AFFICHAGE MESSAGES
function showMessage(message, type = 'info') {
    // Afficher un message d'alerte dynamique
    // Types: 'info', 'success', 'warning', 'danger'
}
```

### Fonctionnalités

| Fonctionnalité | Description | Usage |
|----------------|-------------|-------|
| **Tooltips** | Infobulle au survol | `<button data-bs-toggle="tooltip" title="Info">` |
| **Popovers** | Boîte info cliquable | `<button data-bs-toggle="popover" data-bs-title="Titre">` |
| **Auto-fermeture** | Messages se ferment tout seul | `.alert` (5 secondes) |
| **showMessage()** | Afficher message dynamique | `showMessage("OK!", "success")` |

### Exemple d'Utilisation

```html
<!-- HTML Template -->
<button data-bs-toggle="tooltip" title="Cliquez pour ajouter">
    <i class="fas fa-plus"></i> Ajouter
</button>

<!-- tailor.js initialise automatiquement le tooltip -->
```

---

## 📦 vendor/ - Les Dépendances Externes

### Qu'est-ce que c'est?
**`static/vendor/`** contient **toutes les bibliothèques externes** (frameworks, plugins, etc.) téléchargées et servies **localement** (sans internet).

### Structure du Dossier vendor/

```
vendor/
├── bootstrap/                   # Framework UI Bootstrap
│   ├── css/bootstrap.min.css   # Styles Bootstrap
│   ├── js/bootstrap.bundle.min.js  # Scripts Bootstrap
│   └── ...
│
├── fontawesome/                # Icones Font Awesome
│   ├── css/all.min.css        # Styles icones
│   ├── webfonts/              # Fichiers font
│   │   ├── fa-brands-400.woff2
│   │   ├── fa-solid-900.woff2
│   │   └── fa-regular-400.woff2
│   └── ...
│
├── jquery/                     # Bibliothèque jQuery
│   └── jquery-3.7.0.min.js    # Sélecteurs DOM simplifiés
│
├── chartjs/                    # Graphiques interactifs
│   └── chart.min.js           # Créer des graphes
│
├── datatables/                # Tableaux avancés
│   ├── css/dataTables.bootstrap5.min.css
│   └── js/jquery.dataTables.min.js
│
├── animate/                   # Animations CSS
│   └── animate.min.css       # Effects d'apparition
│
├── toastr/                    # Notifications
│   ├── toastr.min.js         # Afficher notifications
│   └── toastr.min.css
│
├── fonts/                     # Fonts Google (local)
│   ├── fonts.css             # Définition fonts
│   └── files/                # Fichiers TTF/WOFF
│       ├── Montserrat-Regular.ttf
│       ├── PlayfairDisplay-Regular.ttf
│       └── Inter-Regular.ttf
│
├── flatpickr/                # Date picker
│   ├── flatpickr.min.js
│   ├── flatpickr.min.css
│   └── l10n/fr.js           # Locale français
│
├── cleavejs/                 # Formatage inputs
│   └── cleave.min.js        # Masques inputs
│
├── qrcode/                   # QR codes
│   └── qrcode.min.js        # Génération QR
│
└── ... (autres plugins)
```

---

## 🔗 Relation entre tailor.js et vendor/

### Hiérarchie

```
vendor/ (Dépendances externes)
    ├── bootstrap.js
    ├── jquery.js
    ├── chart.js
    └── toastr.js
         ↓
         Utilisées par
         ↓
    tailor.js (Code personnalisé)
         ↓
         Exécuté dans
         ↓
    HTML Templates
```

### Exemple Concret

```html
<!-- base.html -->
<head>
    <!-- Charger les dépendances AVANT tailor.js -->
    <script src="/static/vendor/bootstrap/js/bootstrap.min.js"></script>
    <script src="/static/vendor/jquery/jquery.min.js"></script>
    <script src="/static/vendor/toastr/toastr.min.js"></script>
</head>

<body>
    <!-- Page content -->
    
    <!-- Charger tailor.js APRÈS les dépendances -->
    <script src="/static/js/tailor.js"></script>
    <!-- tailor.js peut maintenant utiliser bootstrap, jquery, toastr -->
</body>
```

---

## 📊 Ce que Contient Réellement vendor/

### Statistiques

```
127 fichiers statiques au total
├── CSS:        18 fichiers  (~1.2 MB)
├── JavaScript: 45 fichiers  (~2.1 MB)
├── Fonts:      8 fichiers   (~1.8 MB)
├── Images:     12 fichiers  (~0.4 MB)
└── Autres:     44 fichiers  (~0.5 MB)

TOTAL: ~6 MB (pour fonctionner sans internet)
```

### Bibliothèques Incluses

| Bibliothèque | Version | Taille | Utilisation |
|--------------|---------|--------|-------------|
| Bootstrap | 5.3.2 | 200 KB | Framework UI complet |
| jQuery | 3.7.0 | 85 KB | Manipulation DOM |
| Font Awesome | 6.4.0 | 240 KB | 2000+ icones |
| Chart.js | Latest | 65 KB | Graphiques |
| DataTables | 1.13.6 | 120 KB | Tables avancées |
| Animate.css | 4.1.1 | 80 KB | Animations |
| Toastr | 2.1.4 | 30 KB | Notifications |
| Flatpickr | Latest | 45 KB | Date picker |
| Cleave.js | Latest | 25 KB | Formatage inputs |
| QRCode | Latest | 20 KB | Codes QR |

---

## 🎨 Cas d'Usage Réels

### 1. Afficher une Notification
```html
<!-- Template HTML -->
<button onclick="showMessage('Client ajouté!', 'success')">
    Ajouter Client
</button>

<!-- tailor.js execute showMessage() -->
```

### 2. Afficher un Tooltip
```html
<!-- Template HTML -->
<button data-bs-toggle="tooltip" title="Créer nouvelle commande">
    <i class="fas fa-plus"></i> Commande
</button>

<!-- tailor.js initialise Bootstrap Tooltip -->
```

### 3. Afficher un Graphique
```html
<!-- Template HTML -->
<canvas id="salesChart"></canvas>

<script>
    // Dans tailor.js ou une page spécifique
    const ctx = document.getElementById('salesChart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: { ... },
        options: { ... }
    });
</script>
```

### 4. Tableau Avancé
```html
<!-- Template HTML -->
<table id="ordersTable" class="table">
    <thead>
        <tr><th>ID</th><th>Client</th><th>Total</th></tr>
    </thead>
    <tbody>
        <!-- Données remplies par Django -->
    </tbody>
</table>

<script>
    // DataTables transforme le tableau en version avancée
    $('#ordersTable').DataTable({
        language: { url: '/static/vendor/datatables/...' }
    });
</script>
```

---

## 🔄 Flux de Chargement

```
1. Navigateur charge la page HTML
         ↓
2. Parse HTML, cherche les ressources
         ↓
3. Charge /static/vendor/*.css (styles)
         ↓
4. Charge /static/css/tailor.css (styles custom)
         ↓
5. Affiche la page (HTML + CSS)
         ↓
6. Charge /static/vendor/*.js (jQuery, Bootstrap, etc)
         ↓
7. Charge /static/js/tailor.js (code custom)
         ↓
8. Exécute DOMContentLoaded dans tailor.js
         ↓
9. Initialise tooltips, popovers, messages
         ↓
10. ✅ Page complètement interactive
```

---

## 💾 Différence: static/ vs staticfiles/

### static/
- **Dossier source** où vous mettez vos fichiers
- Contient vos CSS, JS, vendor personnalisés
- Éditable par les développeurs
- Non servi directement en production

### staticfiles/
- **Dossier généré** par `collectstatic`
- Copie de `static/` optimisée pour la production
- Contient tous les fichiers collectés et minifiés
- Servi par un serveur web statique en production

```bash
# Pour remplir staticfiles/:
python manage.py collectstatic --noinput

# Résultat: Tous les fichiers de static/ sont copiés
```

---

## 🚀 Développement Custom

### Ajouter du JavaScript Custom

**Créer**: `static/js/custom.js`
```javascript
// Votre code personnalisé
document.addEventListener('DOMContentLoaded', function() {
    // Votre logique custom
});
```

**Importer dans template**:
```html
<script src="{% static 'js/custom.js' %}"></script>
```

### Ajouter du CSS Custom

**Créer**: `static/css/custom.css`
```css
/* Votre CSS personnalisé */
.mon-element {
    color: blue;
}
```

**Importer dans template**:
```html
<link rel="stylesheet" href="{% static 'css/custom.css' %}">
```

---

## 📝 Résumé Rapide

| Élément | Rôle | Localisation |
|---------|------|-------------|
| **tailor.js** | Code custom du projet | `/static/js/tailor.js` |
| **vendor/** | Dépendances externes | `/static/vendor/` |
| **Bootstrap** | Framework UI | `/static/vendor/bootstrap/` |
| **jQuery** | Sélecteurs DOM | `/static/vendor/jquery/` |
| **FontAwesome** | Icones | `/static/vendor/fontawesome/` |
| **Chart.js** | Graphiques | `/static/vendor/chartjs/` |
| **DataTables** | Tableaux avancés | `/static/vendor/datatables/` |
| **Fonts** | Typographies locales | `/static/vendor/fonts/` |

---

## 🎓 Points Clés

✅ **tailor.js** = Code personnalisé du projet (petit fichier)
✅ **vendor/** = Toutes les bibliothèques tierces (gros dossier)
✅ **Offline** = Aucune dépendance internet grâce à vendor/ local
✅ **Ordre** = vendor/ chargé AVANT tailor.js
✅ **Développement** = Modifiez tailor.js pour ajouter des fonctionnalités

Besoin d'aide pour ajouter une fonctionnalité? 🚀
