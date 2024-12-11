import pygame
import os
import math

from .base import WorldEntity


class Player(WorldEntity): # Hérite de WorldEntity pour la position dans le monde
    def __init__(self, x, y):
        super().__init__() # Par défaut, le joueur est en (0, 0) dans le monde
        # Dimensions du joueur
        self.width = 30
        self.height = 50

        # Chargement de l'image
        sprite_path = os.path.join("assets", "images", "player.png")
        if os.path.exists(sprite_path):
            self.image = pygame.image.load(sprite_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        else:
            self.image = pygame.Surface([self.width, self.height])
            self.image.fill((255, 0, 0))  # Rectangle rouge par défaut

        self.original_image = self.image  # Garde l'image originale pour la rotation
        self.rect = self.image.get_rect()

        # Position par rapport à la fenêtre
        self.rect.x = x
        self.rect.y = y

        # Marge de déclenchement du scrolling
        self.screen_margin = 100

        # Attributs du joueur
        self.speed = 7
        self.health = 100
        self.max_health = 100
        self.score = 0
        self.is_invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 500  # 1 seconde d'invincibilité après dégât

        # Attributs de l'arme
        self.weapon_damage = 25
        self.weapon_cooldown = 500  # Délai entre les tirs en millisecondes
        self.last_shot_time = 0

        # Direction du joueur (angle en degrés)
        self.angle = 0

    def handle_input(self):
        # Calcul de l'angle vers la souris depuis le centre du joueur
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(-dy, dx))

        self.rect = self.image.get_rect(center=self.rect.center)

        # Mouvement
        keys = pygame.key.get_pressed()

        # On conserve la position actuelle
        old_x = self.rect.x
        old_y = self.rect.y

        # Tentative de mouvement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x = max(100, self.rect.x - self.speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x = min(700, self.rect.x + self.speed)  # 800 - 100
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y = max(100, self.rect.y - self.speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y = min(500, self.rect.y + self.speed)  # 600 - 100

        # Tir
        if pygame.mouse.get_pressed()[0]:  # Clic gauche
            self.shoot()

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.weapon_cooldown:
            self.last_shot_time = current_time
            bullet_speed = 10
            direction_x = math.cos(math.radians(-self.angle))
            direction_y = math.sin(math.radians(-self.angle))

            # On retourne les informations nécessaires pour créer une balle
            return {
                'position': self.rect.center,
                'velocity': (direction_x * bullet_speed, direction_y * bullet_speed),
                'damage': self.weapon_damage
            }
        return None

    def take_damage(self, amount):
        if not self.is_invincible:
            self.health = max(0, self.health - amount)
            self.is_invincible = True
            self.invincible_timer = pygame.time.get_ticks()
            return True
        return False

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def update(self):
        self.handle_input()

        # Gestion de l'invincibilité
        if self.is_invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_timer > self.invincible_duration:
                self.is_invincible = False

    def add_score(self, points):
        self.score += points

    def draw(self, screen):
        # Dessin du joueur
        if self.is_invincible and pygame.time.get_ticks() % 200 < 100:
            # Fait clignoter le joueur quand il est invincible
            return
        screen.blit(self.image, self.rect)

        # Dessin de la barre de vie
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = self.width
        bar_height = 5
        bar_position = (self.rect.x, self.rect.bottom +10)

        # Barre rouge (fond)
        pygame.draw.rect(screen, (255, 0, 0),
                         (bar_position[0], bar_position[1], bar_width, bar_height))
        # Barre verte (santé)
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(screen, (0, 255, 0),
                         (bar_position[0], bar_position[1], health_width, bar_height))

    def get_position(self):
        return self.rect.x, self.rect.y

    def get_center(self):
        return self.rect.center

    def is_alive(self):
        return self.health > 0