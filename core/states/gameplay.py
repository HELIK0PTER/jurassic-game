import pygame
import random
from core.states.state import State
from entities.obstacle import Obstacle
from entities.player import Player
from entities.dinosaur import Dinosaur

# Images des bonus
bonus_images = {
    'speed': pygame.image.load("assets/images/player-bonus1/player_bonus1.png"),
    'fire_rate': pygame.image.load("assets/images/player-bonus2/player_bonus2.png")
}

class Bonus:
    def __init__(self, x, y, bonus_type):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.type = bonus_type

    def get_image(self):
        return bonus_images.get(self.type, None)

    def draw(self, screen):
        screen.blit(self.get_image(), self.rect)


class Gameplay(State):
    def __init__(self, player_name=""):
        super().__init__()
        self.player = Player(375, 275)
        self.enemies = []
        self.bonuses = []
        self.spawn_timer = 0
        self.bonus_timer = 0
        self.player_name = player_name
        self.score = 0
        self.font = pygame.font.Font(None, 36)

        # Initialisation audio
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/background_song.mp3")
        pygame.mixer.music.play(-1)
        self.shoot_sound = pygame.mixer.Sound("assets/sounds/pistolet.ogg")
        self.shoot_sound.set_volume(0.7)

        # Chronomètre pour gérer le délai avant Game Over
        self.gameover_delay = None

        # Charger l'image de fond
        self.background_image = pygame.image.load("assets/images/map/map_background.png")

        # Charger les images des éléments fixes
        self.decor_images = [
            pygame.image.load(f"assets/images/map/{category}/{name}.png")
            for category, names in {
                "trees": ["tree1", "tree2", "tree3", "tree4", "tree5"],
                "rock": ["rock1", "rock2", "rock3"],
                "": ["hole"]
            }.items()
            for name in names
        ]
        self.decor_elements = self.generate_random_decor(grid_size=50)

    def spawn_bonus(self):
        if len(self.bonuses) < 3:
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            bonus_type = random.choice(['speed', 'fire_rate'])
            self.bonuses.append(Bonus(x, y, bonus_type))

    def generate_random_decor(self, grid_size=50):
        decor = []
        map_width, map_height = 800, 600
        for x in range(0, map_width, grid_size):
            for y in range(0, map_height, grid_size):
                if random.random() < 0.1:
                    try:
                        obstacle = Obstacle(x, y)
                        decor.append({"image": obstacle.image, "position": (x, y)})
                    except ValueError:
                        pass
        return decor

    def handle_events(self, events):
        if not self.player.is_dead:
            keys = pygame.key.get_pressed()
            self.player.move(keys)
            mouse_pos = pygame.mouse.get_pos()
            if keys[pygame.K_SPACE]:
                self.player.shoot(mouse_pos, self.shoot_sound)

        for event in events:
            if event.type == pygame.USEREVENT + 1:
                self.player.reset_bonus()
            elif event.type == pygame.USEREVENT + 2:
                self.player.reset_bonus()

    def update(self):
        if not self.player.is_dead:
            # Spawner des ennemis
            self.spawn_timer += 1
            if self.spawn_timer > 120:
                self.enemies.append(Dinosaur())
                self.spawn_timer = 0

            # Gérer l'apparition des bonus
            self.bonus_timer += 1
            if self.bonus_timer > 300:
                self.spawn_bonus()
                self.bonus_timer = 0

            # Mettre à jour les projectiles
            self.player.update_projectiles()

            # Vérifier la collecte des bonus
            for bonus in self.bonuses[:]:
                if self.player.rect.colliderect(bonus.rect):
                    self.player.apply_bonus(bonus.type)
                    self.bonuses.remove(bonus)

            # Mettre à jour les bonus actifs
            self.player.update_bonus()

            # Mettre à jour les ennemis
            self.update_enemies()

    def apply_bonus_effect(self, bonus):
        if bonus.type == 'speed':
            self.player.apply_bonus('speed')
            pygame.time.set_timer(pygame.USEREVENT + 1, 4000)
        elif bonus.type == 'fire_rate':
            self.player.apply_bonus('fire_rate')
            pygame.time.set_timer(pygame.USEREVENT + 2, 5000)

    def update_enemies(self):
        for enemy in self.enemies[:]:
            if enemy.is_dead:
                self.enemies.remove(enemy)
                self.add_score(10)
                continue
            enemy.move_towards_player(self.player.rect)

            for projectile in self.player.projectiles[:]:
                if projectile.rect.colliderect(enemy.rect):
                    self.player.projectiles.remove(projectile)
                    if enemy.take_damage(25):
                        pass  # Placeholder pour une animation ou effet

            if self.player.rect.colliderect(enemy.rect):
                self.player.die()
                self.gameover_delay = pygame.time.get_ticks() + 1000
                pygame.mixer.music.stop()

    def render(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((0, 0, 0))

        # Dessiner l'arrière-plan
        screen_width, screen_height = screen.get_size()
        tile_width, tile_height = self.background_image.get_size()
        for x in range(0, screen_width, tile_width):
            for y in range(0, screen_height, tile_height):
                screen.blit(self.background_image, (x, y))

        # Dessiner les éléments fixes du décor
        for element in self.decor_elements:
            screen.blit(element["image"], element["position"])

        # Dessiner les ennemis, bonus et joueur
        for enemy in self.enemies:
            enemy.draw(screen)
        for bonus in self.bonuses:
            bonus.draw(screen)
        self.player.draw(screen, mouse_pos)

        # Afficher le score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def save_score(self):
        try:
            with open("saves/saved_scores.txt", "a") as file:
                file.write(f"{self.player_name}:{self.score}\n")
            print(f"Score de {self.player_name} ({self.score}) sauvegardé avec succès.")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du score : {e}")

    def add_score(self, amount):
        self.score += amount
