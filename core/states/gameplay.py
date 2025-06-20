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

# Border images
border_images = {
    'up': pygame.image.load("assets/images/map/borders/border_up.png"),
    'down': pygame.image.load("assets/images/map/borders/border_down.png"),
    'left': pygame.image.load("assets/images/map/borders/border_left.png"),
    'right': pygame.image.load("assets/images/map/borders/border_right.png"),
    'upleft': pygame.image.load("assets/images/map/borders/border_upleft.png"),
    'upright': pygame.image.load("assets/images/map/borders/border_upright.png"),
    'downleft': pygame.image.load("assets/images/map/borders/border_downleft.png"),
    'downright': pygame.image.load("assets/images/map/borders/border_downright.png")
}

window_width, window_height = 800, 600

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
        self.enemies = [] # Liste des ennemis sur la carte
        self.bonuses = []  # Liste des bonus sur la carte
        self.spawn_timer = 0
        self.spawn_delay = 120
        self.bonus_timer = 0
        self.player_name = player_name  # Stocke le pseudo du joueur
        self.score = 0
        self.previous_score = 0
        self.difficulty = 1

        # Police générale
        self.font = pygame.font.Font(None, 36)
        # Police spécifique pour les barres de bonus
        self.font_bonus = pygame.font.Font("assets/fonts/SpecialElite-Regular.ttf", 18)

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
        # Coordonnées de la carte (pour déplacer la caméra)
        # [x_min, y_min, x_max, y_max]
        self.map_coords = (-window_width*2, -window_height*2, window_width*2, window_height*2)

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
        if len(self.bonuses) < 20: # max 50 bonus sur la carte
            x = random.randint(self.map_coords[0] + 50, self.map_coords[2] - 50) # Le bonus apparaît dans la carte
            y = random.randint(self.map_coords[1] + 50, self.map_coords[3] - 50) # Le bonus apparaît dans la carte
            choice_type = ['speed', 'fire_rate'][random.randint(0, 1)]
            self.bonuses.append(Bonus(x, y ,choice_type))
            print(f"Bonus {choice_type} apparu en ({x}, {y})")

    def generate_random_decor(self, grid_size=50):
        decor = []
        for x in range(-window_width*2, window_width*2, grid_size):
            for y in range(-window_height*2, window_height*2, grid_size):
                if random.random() < 0.03:
                    try:
                        trying = True
                        while trying:
                            # Si l'obstacle veut apparaître sur un autre obstacle, on le place à côté
                            for element in decor:
                                if element["position"] == (x, y):
                                    x += grid_size
                                    y += grid_size

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

    def move_decor(self, speed, direction):
        for element in self.decor_elements:
            if direction == "up":
                element["position"] = (element["position"][0], element["position"][1] + speed)
            elif direction == "down":
                element["position"] = (element["position"][0], element["position"][1] - speed)
            elif direction == "left":
                element["position"] = (element["position"][0] + speed, element["position"][1])
            elif direction == "right":
                element["position"] = (element["position"][0] - speed, element["position"][1])

    def move_enemies(self, speed, direction):
        for enemy in self.enemies:
            if direction == "up":
                enemy.rect.y += speed
            elif direction == "down":
                enemy.rect.y -= speed
            elif direction == "left":
                enemy.rect.x += speed
            elif direction == "right":
                enemy.rect.x -= speed

    def move_bonus(self, speed, direction):
        for bonus in self.bonuses:
            if direction == "up":
                bonus.rect.y += speed
            elif direction == "down":
                bonus.rect.y -= speed
            elif direction == "left":
                bonus.rect.x += speed
            elif direction == "right":
                bonus.rect.x -= speed

    def handle_events(self, events):
        if not self.player.is_dead:
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
                self.player.shoot(mouse_pos, self.shoot_sound)

            # Gérer le déplacement de la caméra
            marge = 250
            borders = []
            map_borders = []

            # Vérification de toutes les bordures
            if self.player.rect.right > window_width - marge and keys[pygame.K_d]:
                borders.append("right")
                self.move_decor(self.player.speed, "right")
                self.move_enemies(self.player.speed, "right")
                self.move_bonus(self.player.speed, "right")
                self.map_coords = (self.map_coords[0] - self.player.speed, self.map_coords[1],
                                   self.map_coords[2] - self.player.speed, self.map_coords[3])

            if self.player.rect.left < marge and keys[pygame.K_q]:
                borders.append("left")
                self.move_decor(self.player.speed, "left")
                self.move_enemies(self.player.speed, "left")
                self.move_bonus(self.player.speed, "left")
                self.map_coords = (self.map_coords[0] + self.player.speed, self.map_coords[1],
                                   self.map_coords[2] + self.player.speed, self.map_coords[3])

            if self.player.rect.bottom > window_height - marge / 1.5 and keys[pygame.K_s]:
                borders.append("down")
                self.move_decor(self.player.speed, "down")
                self.move_enemies(self.player.speed, "down")
                self.move_bonus(self.player.speed, "down")
                self.map_coords = (self.map_coords[0], self.map_coords[1] - self.player.speed,
                                   self.map_coords[2], self.map_coords[3] - self.player.speed)

            if self.player.rect.top < marge / 1.5 and keys[pygame.K_z]:
                borders.append("up")
                self.move_decor(self.player.speed, "up")
                self.move_enemies(self.player.speed, "up")
                self.move_bonus(self.player.speed, "up")
                self.map_coords = (self.map_coords[0], self.map_coords[1] + self.player.speed,
                                   self.map_coords[2], self.map_coords[3] + self.player.speed)

            # Vérification si le joueur est à la bordure de la carte (sans compter la marge)
            if self.player.rect.right == window_width:
                map_borders.append("right")
            if self.player.rect.left == -window_width:
                map_borders.append("left")
            if self.player.rect.bottom == window_height:
                map_borders.append("down")
            if self.player.rect.top == -window_height:
                map_borders.append("up")

            # Déplacer le joueur avec la liste des bordures et les coordonnées de la carte
            self.player.move(keys, borders, self.map_coords)
            borders.clear()


        for event in events:
            if event.type == pygame.USEREVENT + 1:  # Réinitialiser bonus vitesse
                self.player.reset_speed_bonus()
            elif event.type == pygame.USEREVENT + 2:  # Réinitialiser bonus cadence
                self.player.reset_fire_rate_bonus()

    def update(self):
        if not self.player.is_dead:

            # Spawner des ennemis
            self.spawn_timer += 1
            if self.spawn_timer > self.spawn_delay:
                self.enemies.append(Dinosaur(self.map_coords))
                self.spawn_timer = 0

            # Gérer l'apparition des bonus
            self.bonus_timer += 1
            if self.bonus_timer > 60*1: # Toutes les x secondes (avec x multiplié par 60 pour les ticks)
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
        bar_width = 200
        bar_height = 20
        margin = 10
        border_thickness = 2
        border_radius = 10  # Rayon pour les coins arrondis

        # Positions des barres
        speed_bar_x = screen.get_width() - bar_width - margin
        speed_bar_y = margin
        fire_rate_bar_x = screen.get_width() - bar_width - margin
        fire_rate_bar_y = margin + bar_height + margin

        # Couleurs
        border_color = (0, 0, 0)
        text_color = (0, 0, 0)

        # Dégradés (du côté gauche vers le côté droit)
        # Speed : bleu -> jaune
        speed_start_color = (0, 0, 255)
        speed_end_color = (255, 255, 0)

        # Fire Rate : rouge -> orange
        fire_start_color = (255, 0, 0)
        fire_end_color = (255, 165, 0)

        # Durée totale du bonus (ici 60 * 5 = 300 ticks)
        total_time = 60 * 5

        def create_gradient_surface(width, height, start_color, end_color):
            """Crée une surface avec un dégradé horizontal de start_color à end_color."""
            gradient_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            sr, sg, sb = start_color
            er, eg, eb = end_color

            for x in range(width):
                # Calculer la proportion
                ratio = x / (width - 1) if width > 1 else 0
                # Interpolation linéaire entre les deux couleurs
                r = sr + (er - sr) * ratio
                g = sg + (eg - sg) * ratio
                b = sb + (eb - sb) * ratio
                pygame.draw.line(gradient_surface, (int(r), int(g), int(b)), (x, 0), (x, height))
            return gradient_surface

        def draw_bar(x, y, active_time, start_color, end_color, title):
            # Créer une surface temporaire pour le fond
            temp_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
            # Dessiner un rectangle arrondi semi-transparent sur cette surface
            pygame.draw.rect(temp_surface, (0, 0, 0, 128), (0, 0, bar_width, bar_height), border_radius=border_radius)
            # Blitter cette surface arrondie sur l'écran
            screen.blit(temp_surface, (x, y))

            # Dessiner la bordure arrondie par-dessus
            rect_bar = pygame.Rect(x, y, bar_width, bar_height)
            pygame.draw.rect(screen, border_color, rect_bar, border_thickness, border_radius=border_radius)

            # Calcul de la progression
            if active_time > 0:
                progress = (active_time / total_time) * bar_width
                inner_width = max(int(progress - 2 * border_thickness), 0)
                inner_height = max(bar_height - 2 * border_thickness, 0)

                if inner_width > 0 and inner_height > 0:
                    # Créer la surface de dégradé pour la progression
                    gradient_surf = create_gradient_surface(inner_width, inner_height, start_color, end_color)

                    # Dessiner le dégradé arrondi
                    progress_rect = pygame.Rect(x + border_thickness, y + border_thickness, inner_width, inner_height)
                    # Pour arrondir les coins du dégradé, on peut utiliser un mask ou simplement laisser tel quel.
                    # Ici, on le laisse tel quel, mais le rectangle est à l'intérieur de la barre arrondie, donc ça devrait aller.
                    screen.blit(gradient_surf, progress_rect)

                    # Surbrillance (optionnelle)
                    highlight_width = inner_width
                    highlight_height = inner_height // 2
                    if highlight_width > 0 and highlight_height > 0:
                        highlight_surface = pygame.Surface((highlight_width, highlight_height), pygame.SRCALPHA)
                        highlight_surface.fill((255, 255, 255, 100))
                        screen.blit(highlight_surface, (x + border_thickness, y + border_thickness))

            # Affichage du titre avec la police bonus
            text_surf = self.font_bonus.render(title, True, text_color)
            screen.blit(text_surf, (x + (bar_width - text_surf.get_width()) // 2,
                                    y + (bar_height - text_surf.get_height()) // 2))

        # Dessiner la barre de Speed (dégradé bleu->jaune)
        draw_bar(speed_bar_x, speed_bar_y, self.player.bonus_timers['speed'], speed_start_color, speed_end_color,
                 "Speed")

        # Dessiner la barre de Mini Gun (dégradé rouge->orange)
        draw_bar(fire_rate_bar_x, fire_rate_bar_y, self.player.bonus_timers['fire_rate'], fire_start_color,
                 fire_end_color, "Mini Gun")

    def render_map(self, screen):
        # Dessiner l'arrière plan mer
        screen.fill((0, 0, 255))

        # Dessiner l'arrière-plan terre
        tile_width, tile_height = self.background_image.get_size()
        for x in range(self.map_coords[0], self.map_coords[2], tile_width):  # On dessine 4 fois l'arrière-plan
            for y in range(self.map_coords[1], self.map_coords[3], tile_height):
                screen.blit(self.background_image, (x, y))

        # Dessiner les éléments fixes du décor
        for element in self.decor_elements:
            screen.blit(element["image"], element["position"])

        # Dessiner les bords de la carte
        border_width, border_height = border_images["up"].get_size()
        for x in range(self.map_coords[0], self.map_coords[2], border_width):
            screen.blit(border_images["up"], (x, self.map_coords[1] - border_height))
            screen.blit(border_images["down"], (x, self.map_coords[3]))

        for y in range(self.map_coords[1], self.map_coords[3], border_height):
            screen.blit(border_images["left"], (self.map_coords[0] - border_width, y))
            screen.blit(border_images["right"], (self.map_coords[2], y))

        # Dessiner les coins de la carte
        screen.blit(border_images["upleft"], (self.map_coords[0] - border_width, self.map_coords[1] - border_height))
        screen.blit(border_images["upright"], (self.map_coords[2], self.map_coords[1] - border_height))
        screen.blit(border_images["downleft"], (self.map_coords[0] - border_width, self.map_coords[3]))
        screen.blit(border_images["downright"], (self.map_coords[2], self.map_coords[3]))



    def render(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        # Dessiner la carte
        self.render_map(screen)

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

        # Afficher la difficulté en dessous du score
        difficulty_text = self.font.render(f"Niveau: {self.difficulty}", True, (255, 255, 255))
        screen.blit(difficulty_text, (10, 10 + score_text.get_height() + 5))

    def add_score(self, amount):
        # Augmenter le score
        self.score += amount

        # Vérifier si on a dépassé le prochain seuil de difficulté
        if self.score // 50 > (self.previous_score // 50):
            print("Augmentation de la difficulté !")
            self.difficulty += 1

            # Augmenter la vitesse des ennemis
            for enemy in self.enemies:
                enemy.speed += 0.1

            # Réduire le délai d'apparition des ennemis
            if self.spawn_delay > 30:
                self.spawn_delay -= 5

        # Mettre à jour le score précédent
        self.previous_score = self.score

