import pygame
import random
from core.states.state import State
from entities.player import Player
from entities.dinosaur import Dinosaur

class Bonus:
    def __init__(self, x, y, bonus_type):
        self.rect = pygame.Rect(x, y, 30, 30)  # Taille du bonus
        self.type = bonus_type  # Type de bonus : 'speed', 'fire_rate'
        self.color = self.get_color()

    def get_color(self):
        # Définir une couleur différente pour chaque type de bonus
        if self.type == 'speed':
            return (0, 255, 0)  # Vert
        elif self.type == 'fire_rate':
            return (0, 0, 255)  # Bleu

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Gameplay(State):
    def __init__(self, player_name=""):
        super().__init__()
        self.player = Player(375, 275)
        self.enemies = []
        self.bonuses = []  # Liste des bonus
        self.spawn_timer = 0
        self.bonus_timer = 0  # Timer pour gérer l'apparition des bonus
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

    def spawn_bonus(self):
        if len(self.bonuses) < 3:  # Limiter le nombre de bonus actifs
            x = random.randint(50, 750)  # Position aléatoire
            y = random.randint(50, 550)
            bonus_type = random.choice(['speed', 'fire_rate'])
            self.bonuses.append(Bonus(x, y, bonus_type))

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        mouse_pos = pygame.mouse.get_pos()
        if keys[pygame.K_SPACE]:
            self.player.shoot(mouse_pos, self.shoot_sound)

        for event in events:
            if event.type == pygame.USEREVENT + 1:  # Réinitialiser la vitesse
                self.player.speed = 5
            elif event.type == pygame.USEREVENT + 2:  # Réinitialiser la cadence de tir
                self.player.default_cooldown = 30  # Rétablir la cadence de tir normale

    def update(self):
        # Gérer l'apparition des bonus
        self.bonus_timer += 1
        if self.bonus_timer > 300:  # Tous les 5 secondes (60 FPS)
            self.spawn_bonus()
            self.bonus_timer = 0

        # Vérifier la collecte des bonus
        for bonus in self.bonuses[:]:
            if self.player.rect.colliderect(bonus.rect):
                if bonus.type == 'speed':
                    self.player.speed += 2  # Augmenter la vitesse
                    pygame.time.set_timer(pygame.USEREVENT + 1, 4000)  # Rétablir la vitesse après 5 secondes
                elif bonus.type == 'fire_rate':
                    self.player.default_cooldown = min(5, self.player.default_cooldown // 5)  # Augmenter la cadence
                    pygame.time.set_timer(pygame.USEREVENT + 2, 5000)  # Réinitialiser après 5 secondes
                self.bonuses.remove(bonus)  # Supprimer le bonus collecté

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
        screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()  # Obtenez la position de la souris
        self.player.draw(screen, mouse_pos)  # Passez mouse_pos à la méthode draw
        for enemy in self.enemies:
            enemy.draw(screen)
        for bonus in self.bonuses:
            bonus.draw(screen)  # Dessiner les bonus
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