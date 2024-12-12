import pygame
import random
from core.states.state import State
from entities.player import Player
from entities.dinosaur import Dinosaur

class Gameplay(State):
    def __init__(self, player_name=""):
        super().__init__()
        self.player = Player(375, 275)
        self.enemies = []
        self.spawn_timer = 0
        self.player_name = player_name  # Stocke le pseudo du joueur
        self.score = 0
        self.font = pygame.font.Font(None, 36)

        # Initialisation audio
        pygame.mixer.init()

        # Charger la musique de fond
        pygame.mixer.music.load("assets/sounds/background_song.mp3")
        pygame.mixer.music.play(-1)  # Jouer en boucle
        self.background_music = pygame.mixer.music  # Référence à la musique de fond

        # Charger les sons
        self.shoot_sound = pygame.mixer.Sound("assets/sounds/pistolet.ogg")
        self.shoot_sound.set_volume(0.7)  # Volume normal pour les sons de tir (entre 0 et 1)

        # Chronomètre pour gérer le délai avant Game Over
        self.gameover_delay = None  # Chronomètre avant l'affichage de Game Over

    def handle_events(self, events):
        if not self.player.is_dead:
            keys = pygame.key.get_pressed()
            self.player.move(keys)
            mouse_pos = pygame.mouse.get_pos()
            if keys[pygame.K_SPACE]:
                self.player.shoot(mouse_pos, self.shoot_sound)

    def update(self):
        if not self.player.is_dead:
            # Spawner des ennemis et gestion des projectiles
            self.spawn_timer += 1
            if self.spawn_timer > 120:
                self.enemies.append(Dinosaur())
                self.spawn_timer = 0

            # Mettre à jour les projectiles
            self.player.update_projectiles()

            # Mettre à jour les ennemis
            for enemy in self.enemies[:]:
                if enemy.is_dead:
                    self.enemies.remove(enemy)
                    continue

                # Déplacer le dinosaure vers le joueur
                enemy.move_towards_player(self.player.rect)

                # Gérer les collisions avec les projectiles
                for projectile in self.player.projectiles[:]:
                    if projectile.rect.colliderect(enemy.rect):
                        self.player.projectiles.remove(projectile)
                        if enemy.take_damage(25):
                            pass

                # Si le joueur touche un ennemi
                if self.player.rect.colliderect(enemy.rect):
                    self.player.die()  # Le joueur meurt
                    self.gameover_delay = pygame.time.get_ticks() + 1000  # Attendre 3 secondes avant Game Over
                    pygame.mixer.music.stop()  # Stopper la musique de fond
        # Si le joueur est mort et que le délai est écoulé, aller à l'écran Game Over
        if self.player.is_dead and self.gameover_delay and pygame.time.get_ticks() >= self.gameover_delay:
            self.next_state = "GAMEOVER"
            self.next_state_data = {
                "score": self.score,
                "player_name": self.player_name
            }

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.player.draw(screen)

        # Dessiner les ennemis
        for enemy in self.enemies:
            enemy.draw(screen)

        # Afficher le score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))