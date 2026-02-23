@echo off
REM Script de démarrage Django pour Windows
REM Double-cliquer sur ce fichier pour démarrer l'application

echo ===============================================
echo   TAILOR - Application Django
echo ===============================================
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou non accessible
    echo Installez Python depuis https://www.python.org/downloads/
    echo N'oubliez pas de cocher "Add Python to PATH"
    pause
    exit /b 1
)

REM Activer l'environnement virtuel
if not exist "venv\Scripts\activate.bat" (
    echo [ERREUR] Environnement virtuel non trouvé
    echo Créez-le avec: python -m venv venv
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Afficher le statut
echo [OK] Environnement virtuel activé
python --version

REM Migrer la base de données (une seule fois normalement)
echo.
echo [INFO] Vérification des migrations...
python manage.py migrate --noinput

REM Collecter les statiques
echo [INFO] Collecte des ressources statiques...
python manage.py collectstatic --noinput 2>nul

REM Démarrer le serveur
echo.
echo ===============================================
echo [OK] Démarrage du serveur Django
echo ===============================================
echo.
echo Accédez à l'application:
echo   - Login: http://localhost:8000/users/login/
echo   - Admin: http://localhost:8000/admin/
echo   - Dashboard: http://localhost:8000/dashboard/
echo.
echo Pour arrêter: Ctrl + C
echo.

python manage.py runserver 0.0.0.0:8000

pause
