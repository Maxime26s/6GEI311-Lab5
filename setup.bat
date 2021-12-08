REM Script d'initialisation de l'environnement
REM ajuster le chemin d'acces
set path=%path%;c:\python3;c:\python3\scripts
REM se creer un repertoire a la racine
mkdir a
cd a
REM Creer un environnement virtuel
pip install virtualenv
virtualenv .
REM ou methode alternative
python -m venv .
REM Activer l'environnement
Scripts\activate
REM Recuperer le depot
git clone https://github.com/Maxime26s/6GEI311-Lab5.git
REM Installer les dependances du projet
REM il faut que votre projet ait un fichier requirements.txt
pip install -r requirements.txt
REM Faire votre programme
REM Le lancer avec
py main.py
