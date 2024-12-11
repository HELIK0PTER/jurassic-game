# Jeu Pygame : "Jurassic Car Attack"
## *Auteurs : Matheus, Tom, Jahwin, Gautier*
### *Date de création : 10/12/2024*

## Description du jeu

Dans ce jeu Pygame, vous incarnez une petite voiture qui doit survivre à des vagues de dinosaures tout en accomplissant des objectifs de niveaux. Le joueur contrôle la voiture en utilisant les touches ZQSD et peut se déplacer dans toutes les directions. 

L'objectif est de progresser à travers les niveaux en survivant et en éliminant les dinosaures. À chaque niveau, les défis deviennent de plus en plus difficiles, avec un nombre croissant de dinosaures à tuer et des intervalles de spawn variables.

Un système de caméra avancé permet de suivre les mouvements du joueur, tout en laissant ce dernier se déplacer librement au centre de l'écran jusqu'à une certaine limite.

## Fonctionnalités principales
- **Contrôle du joueur :** Déplacement fluide avec les touches ZQSD.
- **Système de niveaux :** Objectifs progressifs (tuer un certain nombre de dinosaures par niveau).
- **Caméra dynamique :** La caméra bouge lorsque le joueur atteint une certaine distance des bords de l'écran.
- **Gestion de la carte :** Une carte basée sur des tuiles pour un terrain dynamique et adaptable.
- **Système de high score :** Les joueurs entrent leur nom avant de jouer, et leur score (nombre maximum de dinosaures tués) est enregistré.

## Arborescence du projet

```
├── main.py               # Point d'entrée principal
├── assets/               # Ressources (images, sons, etc.)
│   ├── images/           # Images pour les voitures, dinosaures, etc.
│   ├── sounds/           # Sons pour les effets (explosions, collisions)
│   └── fonts/            # Polices personnalisées
├── config.py             # Fichier de configuration (paramètres du jeu)
├── core/                 # Mécaniques et gestion générales
│   ├── camera.py         # Système de caméra
│   ├── events.py         # Gestion des événements (clavier, souris)
│   ├── state.py          # Gestion des états (menus, jeu, pause)
├── entities/             # Entités principales du jeu
│   ├── player.py         # Classe pour la voiture
│   ├── dinosaur.py       # Classe pour les dinosaures
│   └── projectile.py     # Classe pour les projectiles (si applicable)
├── levels/               # Gestion des niveaux
│   ├── level_manager.py  # Logique des niveaux
│   └── level_data.py     # Données spécifiques des niveaux
├── utils/                # Fonctions utilitaires
│   ├── math_utils.py     # Outils mathématiques pour la caméra et collisions
│   ├── spawn_utils.py    # Gestion des spawn des dinosaures
│   └── render_utils.py   # Aide pour le rendu des éléments
├── scores/               # Gestion des scores
│   ├── high_scores.py    # Gestion et affichage des meilleurs scores
│   └── scores_data.json  # Sauvegarde des scores
├── maps/                 # Données des cartes
│   └── map_data.json     # Fichier JSON contenant les données de la carte
└── README.md             # Documentation du projet
```

## Détails techniques

### Caméra
- **Position dynamique :** La caméra suit le joueur lorsque celui-ci dépasse un seuil (par exemple, 100 unités).
- **Impact global :** Tous les objets (dinosaures, projectiles, éléments de la carte) ont une position relative à la caméra.
- **Méthode principale :** `update()` ajuste la position de la caméra et applique un décalage à tous les objets visibles.

### Mouvement du joueur
Le joueur peut se déplacer librement au centre de l'écran tant qu'il reste dans une "zone centrale". Si le joueur dépasse cette zone, la caméra bouge pour suivre le joueur.

### Gestion des niveaux
Les objectifs de chaque niveau (par exemple, tuer 5 dinosaures au niveau 1, 10 au niveau 2) sont définis dans `level_manager.py`. Ces objectifs peuvent inclure :
- Nombre de dinosaures à tuer.
- Intervalle de spawn des ennemis.
- Autres règles spécifiques.

### Carte
La carte utilise une approche basée sur des tuiles, stockée dans un fichier JSON. Exemple :
```json
{
  "tiles": [
    [0, 0, 1, 0],
    [1, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 1, 0, 1]
  ],
  "tile_size": 64
}
```
Chaque numéro représente un type de tuile (par exemple, 0 pour une route, 1 pour un obstacle).

### Système de high score
- **Enregistrement des scores :** Les joueurs saisissent leur nom avant de commencer à jouer.
- **Calcul des scores :** Le score est basé sur le nombre total de dinosaures tués.
- **Sauvegarde :** Les scores sont enregistrés dans un fichier JSON (`scores/scores_data.json`).
- **Affichage :** Les meilleurs scores sont affichés dans un menu dédié.

## Instructions pour commencer

1. **Installation :**
   - Clonez le projet : `git clone <URL>`
   - Installez les dépendances : `pip install -r requirements.txt`

2. **Lancement du jeu :**
   - Exécutez `main.py` : `python main.py`

3. **Contrôles :**
   - ZQSD : Déplacement de la voiture.
   - Évitez les dinosaures et atteignez les objectifs pour passer au niveau suivant.
