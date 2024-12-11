import pygame
from entities.projectile import Projectile
import math

player_sprite_paths = {
    'up': 'assets/images/player/player_up.png',
    'down': 'assets/images/player/player_down.png',
    'left': 'assets/images/player/player_left.png',
    'right': 'assets/images/player/player_right.png',
    'upleft': 'assets/images/player/player_upleft.png',
    'upright': 'assets/images/player/player_upright.png',
    'downleft': 'assets/images/player/player_downleft.png',
    'downright': 'assets/images/player/player_downright.png',
}

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)  # Rectangle représentant le joueur
        self.speed = 5  # Vitesse de déplacement
        self.projectiles = []  # Liste des projectiles tirés par le joueur
        self.shoot_cooldown = 0  # Temps de recharge pour le tir (en frames)
        self.is_dead = False  # Indique si le joueur est mort

        # Charger les sprites
        self.sprites = self.load_sprites(player_sprite_paths)
        self.current_sprite = self.sprites['down']  # Sprite initial
        self.direction = 'down'

    def load_sprites(self, sprite_paths):
        """
        Charge les images de sprites à partir des chemins donnés.
        """
        return {
            'up': pygame.image.load(sprite_paths['up']).convert_alpha(),
            'down': pygame.image.load(sprite_paths['down']).convert_alpha(),
            'left': pygame.image.load(sprite_paths['left']).convert_alpha(),
            'right': pygame.image.load(sprite_paths['right']).convert_alpha(),
            'upleft': pygame.image.load(sprite_paths['upleft']).convert_alpha(),
            'upright': pygame.image.load(sprite_paths['upright']).convert_alpha(),
            'downleft': pygame.image.load(sprite_paths['downleft']).convert_alpha(),
            'downright': pygame.image.load(sprite_paths['downright']).convert_alpha(),
        }

    def move(self, keys):
        """
        Gère le déplacement et la direction.
        """
        dx, dy = 0, 0
        if keys[pygame.K_z]:  # Haut
            dy -= self.speed
        if keys[pygame.K_s]:  # Bas
            dy += self.speed
        if keys[pygame.K_q]:  # Gauche
            dx -= self.speed
        if keys[pygame.K_d]:  # Droite
            dx += self.speed

        # Mise à jour de la position
        self.rect.x += dx
        self.rect.y += dy

        # Déterminer la direction en fonction du mouvement
        if dx > 0 and dy < 0:
            self.direction = 'upright'
        elif dx > 0 and dy > 0:
            self.direction = 'downright'
        elif dx < 0 and dy < 0:
            self.direction = 'upleft'
        elif dx < 0 and dy > 0:
            self.direction = 'downleft'
        elif dx > 0:
            self.direction = 'right'
        elif dx < 0:
            self.direction = 'left'
        elif dy > 0:
            self.direction = 'down'
        elif dy < 0:
            self.direction = 'up'

        # Mettre à jour le sprite courant
        self.current_sprite = self.sprites[self.direction]

    def shoot(self, mouse_pos):
        """
        Tire un projectile en direction de la souris.
        """
        if self.shoot_cooldown == 0:
            dx, dy = mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery
            angle = math.atan2(dy, dx)
            projectile = Projectile(self.rect.centerx, self.rect.centery, angle)
            self.projectiles.append(projectile)
            self.shoot_cooldown = 60 // 2

    def update_projectiles(self):
        """
        Met à jour la position des projectiles.
        """
        for projectile in self.projectiles[:]:
            projectile.move()
            if projectile.rect.bottom < 0 or projectile.rect.top > 600 or projectile.rect.left > 800 or projectile.rect.right < 0:
                self.projectiles.remove(projectile)

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self, screen):
        """
        Dessine le sprite actuel et les projectiles.
        """
        screen.blit(self.current_sprite, (self.rect.x, self.rect.y))
        for projectile in self.projectiles:
            projectile.draw(screen)
