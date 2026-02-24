 Geometry Dash Clone - Pygame
Une réplique du célèbre jeu de plateforme rythmique, développée avec Python et la bibliothèque Pygame. Ce projet met l'accent sur la gestion de la physique, des collisions précises et un système de portails modifiant la gravité.

 Fonctionnalités
Gameplay Dynamique : Saut, collisions et gestion d'une gravité variable.

Système de Portails : Changement de gravité en temps réel (Basse / Haute / Normale) modifiant le comportement du saut.

Gestion d'États : Cycle complet incluant Menu d'accueil, Sélection de niveaux, Mode Jeu, Game Over et Fin de campagne.

Effets Visuels : Système de particules pour les sauts, les portails et les déplacements.

 Architecture du Projet
Le code est organisé de manière modulaire pour faciliter l'ajout de nouveaux obstacles ou mécaniques :

main.py : Point d'entrée du jeu et gestion de la boucle principale.

settings.py : Configuration globale (FPS, couleurs, constantes physiques).

player.py : Logique du joueur (vecteurs de mouvement, rotation, détection au sol).

level.py : Moteur de génération des niveaux et gestion du cycle de vie.

obstacles.py & portals.py : Classes des objets interactifs.

particles.py : Gestionnaire d'effets de particules (poussière, portails).

utils.py : Fonctions utilitaires (chargement d'images, calculs mathématiques).

 Installation et Lancement
Prérequis : Assurez-vous d'avoir Python installé.

Installation de Pygame :

Bash
pip install pygame
Lancer le jeu :

Bash
python main.py
 Commandes
Espace / fleche haut : Sauter

Échap : Retour au menu