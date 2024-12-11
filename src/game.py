import math
import pygame
import random

from src.entities import Player, Dinosaur, Bullet
from src.world.tilemap import World
from game_utils.camera import Camera


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Système de caméra
        self.camera = Camera()

        # Création du monde
        self.world = World(screen.get_width(), screen.get_height())

        # Groupes de sprites
        self.all_sprites = pygame.sprite.Group()
        self.dinosaurs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        # Variables pour le spawn des dinosaures
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = random.randint(6000, 9000)

        self.initialize_game()

    def initialize_game(self):
        # Création du joueur au centre de l'écran
        self.player = Player(self.screen_width // 2, self.screen_height // 2)
        self.all_sprites.add(self.player)

    def handle_shooting(self):
        bullet_info = self.player.shoot()
        if bullet_info:
            # Créer la balle à la position du joueur
            new_bullet = Bullet(
                bullet_info['position'],
                bullet_info['velocity'],
                bullet_info['damage']
            )
            self.bullets.add(new_bullet)
            self.all_sprites.add(new_bullet)

    def update(self):
        # Vérifie si la caméra doit bouger
        camera_movements = self.camera.should_move(
            self.player.rect,
            self.screen_width,
            self.screen_height
        )

        # Si la caméra doit bouger, déplacer tous les objets sauf le joueur
        if any(camera_movements):
            speed = self.player.speed

            # Mise à jour des positions de tous les sprites sauf le joueur
            for sprite in self.all_sprites:
                if sprite != self.player:
                    # Mouvement horizontal
                    if self.camera.moving_left:
                        sprite.rect.x += speed
                    elif self.camera.moving_right:
                        sprite.rect.x -= speed

                    # Mouvement vertical
                    if self.camera.moving_up:
                        sprite.rect.y += speed
                    elif self.camera.moving_down:
                        sprite.rect.y -= speed

            # Mise à jour de la position de la caméra
            self.camera.move_world(speed)

            # Mise à jour du monde (tiles)
            self.world.update(-self.camera.x, -self.camera.y)

        # Mise à jour normale des sprites
        self.all_sprites.update()

        # Vérification des collisions
        self.check_collisions()

    def check_collisions(self):
        # Collisions entre balles et dinosaures
        hits = pygame.sprite.groupcollide(self.bullets, self.dinosaurs, True, False)
        for bullet, dinos in hits.items():
            for dino in dinos:
                dino.take_damage(bullet.damage)
                if dino.health <= 0:
                    self.player.add_score(100)
                    dino.kill()

        # Collisions entre joueur et dinosaures
        if not self.player.is_invincible:
            hits = pygame.sprite.spritecollide(self.player, self.dinosaurs, False)
            for dino in hits:
                if self.player.take_damage(dino.damage):
                    # Effet de recul
                    knockback = 20
                    dx = self.player.rect.centerx - dino.rect.centerx
                    dy = self.player.rect.centery - dino.rect.centery
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist != 0:
                        # S'assurer que le knockback ne pousse pas le joueur hors des limites
                        new_x = self.player.rect.x + (dx / dist) * knockback
                        new_y = self.player.rect.y + (dy / dist) * knockback

                        # Limiter aux marges de l'écran
                        self.player.rect.x = max(100, min(self.screen_width - 100, new_x))
                        self.player.rect.y = max(100, min(self.screen_height - 100, new_y))

    def spawn_dinosaur(self):
        margin = 100

        # Position relative à la vue actuelle de la caméra
        side = random.choice(['left', 'right', 'top', 'bottom'])

        if side == 'left':
            x = -margin
            y = random.randint(0, self.screen_height)
        elif side == 'right':
            x = self.screen_width + margin
            y = random.randint(0, self.screen_height)
        elif side == 'top':
            x = random.randint(0, self.screen_width)
            y = -margin
        else:  # bottom
            x = random.randint(0, self.screen_width)
            y = self.screen_height + margin

        dino = Dinosaur(x, y, self.player)
        self.dinosaurs.add(dino)
        self.all_sprites.add(dino)

    def render(self):
        # Fond noir ou couleur de fond
        self.screen.fill((0, 0, 0))

        # Dessin du monde
        self.world.draw(self.screen)

        # Rendu de tous les sprites
        self.all_sprites.draw(self.screen)

        # Rendu des barres de vie
        for dino in self.dinosaurs:
            dino.draw_health_bar(self.screen)
        self.player.draw_health_bar(self.screen)

        # Interface utilisateur
        font = pygame.font.Font(None, 36)
        # Score
        text = font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        # Timer de spawn et spawn des dinosaures
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_delay:
            self.spawn_dinosaur()
            self.last_spawn_time = current_time
            self.spawn_delay = random.randint(4000, 9000)

        # Affichage du temps avant prochain spawn
        next_spawn = font.render(
            f"Next spawn in: {int((self.spawn_delay - (current_time - self.last_spawn_time)) / 1000)}",
            True, (255, 255, 255)
        )
        self.screen.blit(next_spawn, (10, 50))