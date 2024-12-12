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
        self.type = bonus_type  # Type de bonus : 'speed', 'fire_rate'
        self.rect = self.get_image().get_rect(topleft=(x, y))

    def get_image(self):
        return bonus_images.get(self.type, None)

    def draw(self, screen):
        screen.blit(self.get_image(), self.rect)


class Gameplay(State):
    def __init__(self, player_name=""):
        super().__init__()
        self.player = Player(375, 275)
        self.enemies = []
        self.bonuses = []  # Liste des bonus
        self.spawn_timer = 0
        self.bonus_timer = 0
        self.player_name = player_name  # Stocke le pseudo du joueur
        self.score = 0
        self.font = pygame.font.Font(None, 36)

        # Initialisation audio
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/background_song.mp3")
        pygame.mixer.music.play(-1)

        # Charger les sons
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
        # Générer les éléments du décor du départ
        self.decor_elements = self.generate_random_decor(grid_size=50)

    def spawn_bonus(self):
        if len(self.bonuses) < 3:
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            choice_type = ['speed', 'fire_rate'][random.randint(0, 1)]
            self.bonuses.append(Bonus(x, y ,choice_type))

    def generate_random_decor(self, grid_size=50):
        decor = []
        map_width, map_height = 800, 600
        for x in range(0, map_width, grid_size):
            for y in range(0, map_height, grid_size):
                if random.random() < 0.03:
                    try:
                        trying = True
                        while trying:
                            # Si l'obstacle veut apparaître sur un autre obstacle, on le place à côté
                            for element in decor:
                                if element["position"] == (x, y):
                                    x += grid_size
                                    y += grid_size
                                    break
                            # Si l'obstacle veut apparaître sur le joueur, on le met pas
                            if self.player.rect.colliderect(pygame.Rect(x, y, grid_size, grid_size)):
                                x = None
                                y = None
                            # Si les étapes précédentes sont passées, on ajoute l'obstacle
                            if x is not None and y is not None:
                                obstacle = Obstacle(x, y)
                                decor.append({"image": obstacle.image, "position": (x, y)})
                            trying = False
                    except ValueError:
                        pass
        return decor

    def handle_events(self, events):
        if not self.player.is_dead:
            keys = pygame.key.get_pressed()
            self.player.move(keys)
            mouse_pos = pygame.mouse.get_pos()
            if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
                self.player.shoot(mouse_pos, self.shoot_sound)

        for event in events:
            if event.type == pygame.USEREVENT + 1:  # Réinitialiser bonus vitesse
                self.player.reset_speed_bonus()
            elif event.type == pygame.USEREVENT + 2:  # Réinitialiser bonus cadence
                self.player.reset_fire_rate_bonus()

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

        if self.gameover_delay is not None:
            self.gameover_delay -= 1
            if self.gameover_delay <= 0:
                self.next_state = "GAMEOVER"

        # Mise à jour du score
        if pygame.time.get_ticks() % 60 == 0:
            self.add_score(1)

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
                        pass

            if self.player.rect.colliderect(enemy.rect):
                self.player.die()
                self.gameover_delay = 60
                pygame.mixer.music.stop()

    def render_bonus_bars(self, screen):
        """Dessine les barres de progression des bonus en haut à droite de l'écran."""
        bar_width = 200
        bar_height = 20
        margin = 10
        border_thickness = 2

        # Position des barres
        speed_bar_x = screen.get_width() - bar_width - margin
        speed_bar_y = margin
        fire_rate_bar_x = screen.get_width() - bar_width - margin
        fire_rate_bar_y = margin + bar_height + margin

        # Barre de vitesse
        # Dessiner le fond de la barre
        pygame.draw.rect(screen, (50, 50, 50), (speed_bar_x, speed_bar_y, bar_width, bar_height))
        # Dessiner la bordure
        pygame.draw.rect(screen, (255, 255, 255), (speed_bar_x, speed_bar_y, bar_width, bar_height), border_thickness)

        # Dessiner la progression si le bonus est actif
        if self.player.bonus_timers['speed'] > 0:
            speed_progress = (self.player.bonus_timers['speed'] / (60 * 5)) * bar_width
            pygame.draw.rect(screen, (255, 255, 0), (speed_bar_x + border_thickness, speed_bar_y + border_thickness,
                                                     speed_progress - 2 * border_thickness,
                                                     bar_height - 2 * border_thickness))

        # Texte "Speed" toujours affiché
        speed_text = self.font.render("Speed", True, (255, 255, 255))
        screen.blit(speed_text, (speed_bar_x + (bar_width - speed_text.get_width()) // 2,
                                 speed_bar_y + (bar_height - speed_text.get_height()) // 2))

        # Barre de cadence de tir
        # Dessiner le fond de la barre
        pygame.draw.rect(screen, (50, 50, 50), (fire_rate_bar_x, fire_rate_bar_y, bar_width, bar_height))
        # Dessiner la bordure
        pygame.draw.rect(screen, (255, 255, 255), (fire_rate_bar_x, fire_rate_bar_y, bar_width, bar_height),
                         border_thickness)

        # Dessiner la progression si le bonus est actif
        if self.player.bonus_timers['fire_rate'] > 0:
            fire_rate_progress = (self.player.bonus_timers['fire_rate'] / (60 * 5)) * bar_width
            pygame.draw.rect(screen, (128, 128, 128),
                             (fire_rate_bar_x + border_thickness, fire_rate_bar_y + border_thickness,
                              fire_rate_progress - 2 * border_thickness, bar_height - 2 * border_thickness))

        # Texte "Mini Gun" toujours affiché
        fire_rate_text = self.font.render("Mini Gun", True, (255, 255, 255))
        screen.blit(fire_rate_text, (fire_rate_bar_x + (bar_width - fire_rate_text.get_width()) // 2,
                                     fire_rate_bar_y + (bar_height - fire_rate_text.get_height()) // 2))

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

        # Dessiner les barres de progression des bonus
        self.render_bonus_bars(screen)

        # Afficher le score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def add_score(self, amount):
        self.score += amount
