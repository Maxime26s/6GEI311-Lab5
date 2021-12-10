REM Script d'initialisation de l'environnement
REM Ajuster le chemin d'acces
set path=%path%;c:\python3;c:\python3\scripts
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