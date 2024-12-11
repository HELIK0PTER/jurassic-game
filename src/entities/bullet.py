# entities/bullet.py
import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, velocity, damage):
        super().__init__()
        # Création du projectile
        self.width = 8
        self.height = 8
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255, 255, 0))  # Couleur jaune

        # Rectangle de collision
        self.rect = self.image.get_rect()
        self.rect.center = position

        # Position mondiale
        self.world_x = position[0]
        self.world_y = position[1]

        # Propriétés du projectile
        self.velocity = velocity
        self.damage = damage
        self.lifetime = 1000  # Durée de vie en millisecondes
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        # Mise à jour de la position mondiale
        self.world_x += self.velocity[0]
        self.world_y += self.velocity[1]

        # Vérification de la durée de vie
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

        # La position du rect sera mise à jour dans Game.update()