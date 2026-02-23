# Mode Hors Ligne - Configuration Locale

Ce projet est maintenant configuré pour fonctionner **sans connexion Internet** avec toutes les ressources locales.

## Configuration

### 1. **Ressources Statiques Locales**

Toutes les dépendances CDN ont été remplacées par des versions locales :
- **Bootstrap 5** : `/static/vendor/bootstrap/`
- **Font Awesome 6** : `/static/vendor/fontawesome/`
- **jQuery 3.7** : `/static/vendor/jquery/`
- **Chart.js** : `/static/vendor/chartjs/`
- **DataTables** : `/static/vendor/datatables/`
- **Animate.css** : `/static/vendor/animate/`
- **Toastr** : `/static/vendor/toastr/`
- **Fonts** : `/static/vendor/fonts/`

### 2. **Configuration Django**

Fichiers modifiés:
- `config/settings/base.py` - Ajout de `STATICFILES_DIRS`
- `templates/base.html` - Remplacement des CDN par versions locales
- `templates/404.html` - Remplacement des CDN
- Templates applicatifs - Remplacement des CDN dans 12+ templates

### 3. **Démarrer en Mode Offline**

Utilisez le script fourni:
```bash
./run_dev.sh
```

Ou manuellement:
```bash
export DJANGO_SETTINGS_MODULE=config.settings.development
python manage.py runserver 0.0.0.0:8000
```

## Vérification

Pour vérifier que tout est en local, consultez les logs ou visitez:
```
http://localhost:8000/users/login/
```

Regardez le code source de la page (Ctrl+U / Cmd+U) et cherchez `/static/vendor/` - vous ne devriez voir **aucune référence à** `https://cdn`, `https://fonts.googleapis`, `https://code.jquery` ou `https://cdnjs`.

## Ressources Incluses

Le dossier `/static/vendor/` contient maintenant :
- **127 fichiers statiques** collectés via `python manage.py collectstatic`
- Tous les webfonts pour Font Awesome
- Tous les CSS et JS minifiés
- Fichiers de configuration pour Flatpickr, QRCode, Cleave.js, etc.

## Performance en Mode Offline

- ✓ Aucune latence CDN
- ✓ Chargement instant des styles et scripts
- ✓ Fonctionnement 100% sans internet

## Notes

- Les bases de données locales (SQLite) restent inchangées
- Les uploads utilisateur (MEDIA_ROOT) restent locaux
- Toutes les fonts Google sont maintenant servies depuis `/static/vendor/fonts/`
