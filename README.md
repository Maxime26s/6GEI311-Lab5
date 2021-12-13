# 6GEI311 - Projet de conception
## Auteurs
Alan Brucher et Maxime Simard

## Prérequis
Python >= 3.9

## Installation

### Installer le logiciel

#### Si le projet n'est pas cloner
- Télécharger le fichier "install.bat".
- Run le fichier "install.bat" pour cloner le projet, installer l'environnement virtuel et ses dépendances.
- Run le fichier "run.bat" dans le dossier 6GEI311-Lab5 pour exécuter le programme.

#### Si le projet est cloner
- Run le fichier "setup.bat" dans le dossier 6GEI311-Lab5 pour installer l'environnement virtuel et ses dépendances.
- Run le fichier "run.bat" dans le dossier 6GEI311-Lab5 pour exécuter le programme.

## Utilisation

### Envoyer une Alerte 

- Sélectionnez le bouton “Set Alert” 
- Entrez le mail et/ou le numéro de téléphone où l’alerte doit être envoyé 
- Confirmer 

### Modifier les options 

- Sélectionnez le bouton “Options” 
- Modifier les options de chaque variable : 
  - Threshold (0-255) : quantité de changement nécessaire pour être considéré comme un mouvement (0 étant tout est un mouvement et 255 étant rien n'est un mouvement) 
  - Framerate (0-infini) : à 0, update l'image à chaque occasion. À une autre valeur, update l'image à ce framerate. 
  - Scale ratio (float) : À quel point sera compressé l'image lors de la détection des formes 
  - Compression (float) : À quel point sera compressé l'image lors du filtrage du mouvement 
  - Alogrithme : quel algorithme sera utilisé 
  - Kernel size (nombre impair >= 1) : Taille du kernel du filtre gaussien (modifié) 
  - Background image buffer (entier) : taille du buffer d'image de background 
  - Motion image buffer (entier) : taille du buffer d'image de mouvement 
  - Motion size devrait être plus petit que background size 
  - Min size ratio (float) : pourcentage de l'image qu'un mouvement détecté devrait être plus grand ou égale à pour être considéré comme un mouvement 
  - Combine (checkbox) : est-ce que les boites devraient être combiné si elles se touchent 
- Confirmez 

### Stats de la vidéo 

- Sélectionnez le bouton “Stats” 
- Affiche le nom et la moyenne de chaque variable de l’algorithme 

### Filtre de la vidéo 

- Sélectionnez le bouton “Motion filter” 
- Affiche le filtre de détection de l’algorithme 

### Sélectionner la source de la vidéo 

- Sélectionnez le bouton “Source” 
- Pour une vidéo locale, appuyez sur le bouton “Browse” et sélectionner le fichier vidéo. Des exemples de fichier vidéo sont disponible dans le dossier “Vidéos” du projet. 
- Pour une vidéo via un lien de camera IP, coller le lien dans l’entrée. Des exemples de lien sont disponibles dans le fichier texte “videos_link.txt”. 
- Confirmer la sélection 

## Sources

- I. Kudriavtsev. [« High-Performance Noise-tolerant Motion Detector in Python, OpenCV, and Numba. »](https://bitworks.software/en/high-speed-movement-detector-opencv-numba-numpy-python.html)
- Scikit-image. [« scikit-image: image processing in python. »](https://scikit-image.org/)

## License
[MIT](https://choosealicense.com/licenses/mit/)
