#!/bin/bash

# ===================================================
# TAILOR - Atelier de Couture Management System
# Script de Lancement - Linux/macOS
# ===================================================

# Chemin vers le dossier du projet
PROJECT_DIR="/home/demba/dev/django/tailor"

# Couleurs pour l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     TAILOR - Gestion d'Atelier de Couture            ║${NC}"
echo -e "${BLUE}║          Démarrage de l'Application                   ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

# Vérifier que le dossier existe
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}✗ Erreur: Le dossier du projet n'existe pas${NC}"
    echo -e "  ${YELLOW}Chemin: $PROJECT_DIR${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Dossier du projet trouvé${NC}"

# Aller au dossier du projet
cd "$PROJECT_DIR" || exit 1

# Vérifier que l'environnement virtuel existe
if [ ! -f "venv/bin/activate" ]; then
    echo -e "${RED}✗ Erreur: Environnement virtuel non trouvé${NC}"
    echo -e "${YELLOW}  Créez-le avec: python3 -m venv venv${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Environnement virtuel trouvé${NC}"

# Activation de l'environnement virtuel
echo -e "${BLUE}→ Activation de l'environnement virtuel...${NC}"
source venv/bin/activate

# Vérifier que Django est installé
if ! python -m django --version >/dev/null 2>&1; then
    echo -e "${RED}✗ Erreur: Django n'est pas installé${NC}"
    echo -e "${YELLOW}  Installez les dépendances: pip install -r requirements.txt${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Django est prêt${NC}"

# Libérer le port 8000 s'il est déjà utilisé
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${YELLOW}⚠ Le port 8000 est déjà utilisé, libération...${NC}"
    fuser -k 8000/tcp 2>/dev/null
    sleep 1
fi

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}✓ Tous les contrôles sont passés${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

# Ouvrir le navigateur
echo -e "${BLUE}→ Ouverture du navigateur...${NC}"
echo ""

# Vérifier les navigateurs disponibles
if command -v google-chrome &> /dev/null; then
    BROWSER="google-chrome"
    BROWSER_NAME="Chrome"
elif command -v chromium &> /dev/null; then
    BROWSER="chromium"
    BROWSER_NAME="Chromium"
elif command -v firefox &> /dev/null; then
    BROWSER="firefox"
    BROWSER_NAME="Firefox"
elif command -v firefox-bin &> /dev/null; then
    BROWSER="firefox-bin"
    BROWSER_NAME="Firefox"
else
    BROWSER=""
    BROWSER_NAME="Aucun"
fi

if [ -z "$BROWSER" ]; then
    echo -e "${YELLOW}⚠ Aucun navigateur détecté${NC}"
    echo -e "  Ouvrez manuellement: ${BLUE}http://127.0.0.1:8000${NC}"
else
    echo -e "${GREEN}✓ Navigateur trouvé: $BROWSER_NAME${NC}"
    # Ouvrir le navigateur après 2 secondes
    (sleep 2 && $BROWSER --app=http://127.0.0.1:8000 2>/dev/null) &
fi

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}✓ Démarrage du serveur Django...${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Accédez à l'application:${NC}"
echo -e "  - ${BLUE}Login: http://127.0.0.1:8000/users/login/${NC}"
echo -e "  - ${BLUE}Admin: http://127.0.0.1:8000/admin/${NC}"
echo -e "  - ${BLUE}Dashboard: http://127.0.0.1:8000/dashboard/${NC}"
echo ""
echo -e "${YELLOW}Pour arrêter: Ctrl + C${NC}"
echo ""

# Lancement du serveur Django
python manage.py runserver 0.0.0.0:8000
