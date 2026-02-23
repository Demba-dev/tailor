# 🚀 Démarrage Rapide

## Linux / macOS

```bash
# 1. Cloner le projet
git clone https://github.com/yourrepo/tailor.git
cd tailor

# 2. Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Migrer la base de données
python manage.py migrate
python manage.py createsuperuser

# 5. Collecter les statiques
python manage.py collectstatic --noinput

# 6. Démarrer l'app
./run_dev.sh

# ou:
python manage.py runserver
```

**Accédez à**: http://localhost:8000/users/login/

---

## Windows

```cmd
# 1. Cloner le projet
git clone https://github.com/yourrepo/tailor.git
cd tailor

# 2. Créer environnement virtuel
python -m venv venv
venv\Scripts\activate.bat

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Migrer la base de données
python manage.py migrate
python manage.py createsuperuser

# 5. Collecter les statiques
python manage.py collectstatic --noinput

# 6. Démarrer l'app
run_dev.bat

# ou:
python manage.py runserver
```

**Accédez à**: http://localhost:8000/users/login/

---

## Comparaison Rapide

| Tâche | Linux/macOS | Windows |
|-------|-----------|---------|
| Créer venv | `python3 -m venv venv` | `python -m venv venv` |
| Activer venv | `source venv/bin/activate` | `venv\Scripts\activate.bat` |
| Démarrer l'app | `./run_dev.sh` | `run_dev.bat` |
| Port 8000 utilisé | `lsof -i :8000` | `netstat -ano \| findstr :8000` |
| Tuer processus | `kill <PID>` | `taskkill /PID <PID> /F` |
| Chemin Python venv | `venv/bin/python` | `venv\Scripts\python.exe` |

---

## ✅ Checklist Finale

### Installation
- [ ] Python 3.11+ installé
- [ ] Git installé (pour cloner)
- [ ] Projet cloné
- [ ] Environnement virtuel créé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Migrations appliquées (`python manage.py migrate`)
- [ ] Superuser créé
- [ ] Statiques collectés

### Démarrage
- [ ] Environnement virtuel activé
- [ ] Serveur démarré (`python manage.py runserver`)
- [ ] Aucune erreur dans le terminal
- [ ] http://localhost:8000/users/login/ accessible

### Vérification Offline
- [ ] Pas de CDN détecté (grep "https://cdn")
- [ ] Ressources locales chargées (/static/vendor/)
- [ ] CSS/JS appliqués correctement
- [ ] Fonts affichées correctement

---

## 📖 Documentation Complète

- **WINDOWS_SETUP.md** - Guide détaillé pour Windows
- **OFFLINE_MODE.md** - Fonctionnement sans internet
- **PROCEDURES_OFFLINE.md** - Procédures de configuration
- **CLAUDE.md** - Notes de développement (si existe)

---

## 🆘 Aide Rapide

**Erreur: "python" non reconnu**
```bash
# Linux/macOS
which python3

# Windows
where python
```

**Erreur: "venv" non trouvé**
```bash
# Recréer l'environnement virtuel
python -m venv venv
```

**Erreur: Port 8000 utilisé**
```bash
# Utiliser un autre port
python manage.py runserver 8080
```

**Erreur: Base de données corrompue**
```bash
# Supprimer et recréer
rm db.sqlite3  # Linux/macOS
# ou
del db.sqlite3  # Windows

python manage.py migrate
python manage.py createsuperuser
```

---

## 🎯 Prochaines Étapes

1. ✅ Application démarrée
2. 📝 Modifier les templates dans `templates/`
3. 🔧 Créer de nouvelles apps avec `python manage.py startapp nom_app`
4. 💾 Pusher les changements sur Git
5. 🚀 Déployer (guide séparé)

---

## 💬 Support

- 📚 Documentation Django: https://docs.djangoproject.com/
- 🐛 Issues: Vérifier le projet Git
- 🔍 Logs: Regarder le terminal du serveur

Bon développement! 🚀
