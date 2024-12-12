import pygame
from random import randint, choice

# Définir les obstacles disponibles
obstacles = [
    {
        "nom": "arbre 1",
        "image": "assets/images/map/trees/tree1.png",
        "type": "arbre"
    },
    {
        "nom": "arbre 2",
        "image": "assets/images/map/trees/tree2.png",
        "type": "arbre"
    },
    {
        "nom": "rocher 1",
        "image": "assets/images/map/rock/rock1.png",
        "type": "rocher"
    },
    {
        "nom": "rocher 2",
        "image": "assets/images/map/rock/rock2.png",
        "type": "rocher"
    }
]

# Liste des types, pour pondérer les probabilités de chaque type d'obstacle
types = ["arbre", "arbre", "arbre", "rocher", "rocher"]

def choisir_obstacle():
    """
    Sélectionne un obstacle aléatoire en fonction des types disponibles.
    :return: Un dictionnaire représentant l'obstacle choisi.
    """
    choix_type = choice(types)  # Choisir un type aléatoire
    obstacles_du_type = [obs for obs in obstacles if obs["type"] == choix_type]
    return choice(obstacles_du_type) if obstacles_du_type else None

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Choisir un obstacle aléatoire
        obstacle_data = choisir_obstacle()
        if obstacle_data:
            self.image = pygame.image.load(obstacle_data["image"]).convert_alpha()
            self.rect = self.image.get_rect(topleft=(x, y))
        else:
            raise ValueError("Aucun obstacle valide n'a été trouvé.")

    def draw(self, screen):
        """
        Dessine l'obstacle sur l'écran.
        :param screen: Surface de l'écran de jeu.
        """
        screen.blit(self.image, self.rect.topleft)