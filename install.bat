REM Script d'initialisation de l'environnement
REM Ajuster le chemin d'acces
set path=%path%;c:\python3;c:\python3\scripts
REM Récupère le projet du repository GitHub
git clone https://github.com/Maxime26s/6GEI311-Lab5.git
cd 6GEI311-Lab5
REM Creer un repertoire
mkdir venv
cd venv
REM Creer un environnement virtuel
pip install virtualenv
virtualenv .
REM Activer l'environnement
call .\Scripts\activate
cd ..
REM Installe les dépendances du fichier requirements.txt
pip install -r requirements.txt
REM Exécute le programme
py main.py