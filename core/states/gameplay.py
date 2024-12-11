import pygame
import random
from core.states.state import State
from entities.player import Player
from entities.dinosaur import Dinosaur

sprite_paths = {
    'up': 'assets/images/player_up.png',
    'down': 'assets/images/player_down.png',
    'left': 'assets/images/player_left.png',
    'right': 'assets/images/player_right.png',
    'upleft': 'assets/images/player_upleft.png',
    'upright': 'assets/images/player_upright.png',
    'downleft': 'assets/images/player_downleft.png',
    'downright': 'assets/images/player_downright.png',
}

class Gameplay(State):
    def __init__(self, player_name = ""):
        super().__init__()
        self.player = Player(375, 275, sprite_paths)
        self.enemies = []
        self.spawn_timer = 0
        self.player_name = player_name
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        mouse_pos = pygame.mouse.get_pos()
        if keys[pygame.K_SPACE]:
            self.player.shoot(mouse_pos)

    def update(self):
        # Spawner des ennemis
        self.spawn_timer += 1
        if self.spawn_timer > 120:
            self.enemies.append(Dinosaur())
            self.spawn_timer = 0

        # Mettre à jour les projectiles
        self.player.update_projectiles()

        # Mettre à jour les ennemis
        for enemy in self.enemies[:]:
            enemy.move_towards_player(self.player.rect)

            for projectile in self.player.projectiles[:]:
                if projectile.rect.colliderect(enemy.rect):
                    self.player.projectiles.remove(projectile)
                    if enemy.take_damage(25):
                        self.enemies.remove(enemy)

            # si le joueur touche un ennemi, reset tout le jeu et passer à l'écran de game over
            if self.player.rect.colliderect(enemy.rect):
                # clear les ennemis
                self.enemies.clear()
                # reset la position du joueur
                self.player.rect.x = 375
                self.player.rect.y = 275
                self.next_state = "GAMEOVER"

        # Mettre à jour le score tous les 60 ticks
        if pygame.time.get_ticks() % 60 == 0:
            self.add_score(1)

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def add_score(self, amount):
        self.score += amount