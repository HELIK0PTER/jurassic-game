# entities/dinosaur.py
import pygame
import random
import math


class Dinosaur(pygame.sprite.Sprite):
    def __init__(self, world_x, world_y, player):
        super().__init__()
        # Dimensions du dinosaure
        self.width = 50
        self.height = 50

        # Création de l'image
        self.image = pygame.Surface([self.width, self.height])

        # Position dans le monde
        self.world_x = world_x
        self.world_y = world_y

        # Rectangle de collision
        self.rect = self.image.get_rect()
        self.rect.x = world_x
        self.rect.y = world_y

        # Référence au joueur pour le suivi
        self.player = player

        # Attributs du dinosaure
        self.speed = 3
        self.detection_range = 200
        self.is_active = False
        self.health = 100
        self.damage = 20

        # Type de dinosaure et setup
        self.dino_type = random.choice(['raptor', 'trex', 'ptero'])
        self.setup_dino_type()

    def setup_dino_type(self):
        if self.dino_type == 'raptor':
            self.speed = 4
            self.damage = 15
            self.health = 80
            self.image.fill((0, 100, 0))  # Vert foncé
        elif self.dino_type == 'trex':
            self.speed = 2
            self.damage = 40
            self.health = 150
            self.image.fill((139, 0, 0))  # Rouge foncé
        else:  # ptero
            self.speed = 5
            self.damage = 10
            self.health = 60
            self.image.fill((70, 130, 180))  # Bleu

    def distance_to_player(self):
        return math.sqrt(
            (self.world_x - self.player.rect.centerx) ** 2 +
            (self.world_y - self.player.rect.centery) ** 2
        )

    def move_towards_player(self):
        # Calculer la direction vers le joueur en utilisant les coordonnées mondiales
        dx = self.player.rect.centerx - self.world_x
        dy = self.player.rect.centery - self.world_y

        # Normaliser la distance
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            dx = dx / distance
            dy = dy / distance

            # Mise à jour de la position mondiale
            self.world_x += dx * self.speed
            self.world_y += dy * self.speed

    def update(self):
        distance = self.distance_to_player()

        # Vérifier si le dinosaure doit devenir actif
        if not self.is_active and distance < self.detection_range:
            self.is_active = True

        # Si actif, poursuivre le joueur
        if self.is_active:
            self.move_towards_player()

            # Comportement spécifique selon le type
            if self.dino_type == 'raptor':
                if distance < 100:
                    self.speed = 5
                else:
                    self.speed = 4
            elif self.dino_type == 'ptero':
                self.world_x += math.sin(pygame.time.get_ticks() * 0.01) * 2

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def draw_health_bar(self, screen):
        health_ratio = self.health / 100
        bar_width = self.width
        bar_height = 5
        bar_position = (self.rect.x, self.rect.y - 10)

        # Barre rouge (fond)
        pygame.draw.rect(screen, (255, 0, 0),
                         (bar_position[0], bar_position[1], bar_width, bar_height))
        # Barre verte (santé)
        pygame.draw.rect(screen, (0, 255, 0),
                         (bar_position[0], bar_position[1],
                          bar_width * health_ratio, bar_height))