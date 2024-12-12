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

        # Charger l'image de fond
        self.background_image = pygame.image.load("assets/images/map/map_background.png")

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        mouse_pos = pygame.mouse.get_pos()
        if keys[pygame.K_SPACE]:
            self.player.shoot(mouse_pos, self.shoot_sound)

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

            # Si le joueur touche un ennemi, transition vers l'écran de game over
            if self.player.rect.colliderect(enemy.rect):
                # Arrêter complètement la musique de fond
                pygame.mixer.music.stop()
                self.enemies.clear()  # Clear les ennemis
                self.player.rect.x = 375  # Reset la position du joueur
                self.player.rect.y = 275
                # Passer à l'état GameOver avec le score et le pseudo
                self.next_state = "GAMEOVER"
                self.next_state_data = {
                    "score": self.score,
                    "player_name": self.player_name  # Transmission du pseudo
                }
                return  # Arrêter le reste de l'exécution de cette frame

        # Mettre à jour le score tous les 60 ticks
        if pygame.time.get_ticks() % 60 == 0:
            self.add_score(1)

    def render(self, screen):
        # Obtenir la taille de l'écran et de l'image
        screen_width, screen_height = screen.get_size()
        tile_width, tile_height = self.background_image.get_size()

        # Dessiner le fond de manière répétitive
        for x in range(0, screen_width, tile_width):
            for y in range(0, screen_height, tile_height):
                screen.blit(self.background_image, (x, y))

        # Dessiner les entités
        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)

        # Dessiner le score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def save_score(self):
        """Sauvegarde le score actuel dans le fichier `saves/saved_scores.txt`."""
        try:
            with open("saves/saved_scores.txt", "a") as file:
                file.write(f"{self.player_name}:{self.score}\n")
            print(f"Score de {self.player_name} ({self.score}) sauvegardé avec succès.")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du score : {e}")

    def add_score(self, amount):
        self.score += amount
