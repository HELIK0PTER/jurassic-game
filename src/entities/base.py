import pygame

class WorldEntity(pygame.sprite.Sprite):
    """Classe de base pour toutes les entités ayant une position dans le monde"""

    def __init__(self, world_x = 0, world_y = 0):
        super().__init__()
        # Position dans le monde
        self.world_x = world_x
        self.world_y = world_y
        self.image = pygame.Surface([0, 0])  # Doit être redéfini dans les classes filles

        # Le rect est uniquement utilisé pour l'affichage et les collisions
        self.rect = self.image.get_rect()
        self.rect.x = world_x  # Sera mis à jour par la caméra
        self.rect.y = world_y
