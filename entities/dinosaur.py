import pygame
import random

class Dinosaur:
    def __init__(self, map_cords = [0,0,0,0]):
        self.map_cords = map_cords
        print("spawn at ",map_cords)
        self.dino_type = random.choice(["DinoNormal", "DinoRapide", "DinoLent"])
        self.configure_dinosaur()

        # Initialiser les variables nécessaires pour l'animation
        self.current_frame = 0
        self.image = self.animation_frames[int(self.current_frame)]
        self.rect = self.image.get_rect()

        self.random_spawn()
        self.direction = "right"

        # Attributs pour gérer la mort et l'explosion
        self.is_dead = False  # Le dinosaure n'est pas mort au départ
        self.explosion_frames = []  # Frames d'explosion
        self.explosion_frame = 0
        self.explosion_finished = False  # Pour savoir si l'explosion est terminée

        # Charger les images de l'explosion (ajoute tes propres images ici)
        for i in range(1, 3):
            self.explosion_frames.append(pygame.image.load(f"assets/images/Dino/exploD{i}.png"))

        # Charger le son de l'explosion
        self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.mp3")
        self.explosion_sound.set_volume(0.7)  # Ajuste le volume à ton goût

    def configure_dinosaur(self):
        if self.dino_type == "DinoNormal":
            self.animation_frames = [
                pygame.image.load(f"assets/images/Dino/DinoNormal{i}.png") for i in range(1, 6)
            ]
            self.speed = 1
            self.health = 100
            self.max_health = 100
            self.size = (70, 50)
        elif self.dino_type == "DinoRapide":
            self.animation_frames = [
                pygame.image.load(f"assets/images/Dino/DinoRapide{i}.png") for i in range(1, 10)
            ]
            self.speed = 2
            self.health = 25
            self.max_health = 25
            self.size = (50, 30)
        elif self.dino_type == "DinoLent":
            self.animation_frames = [
                pygame.image.load(f"assets/images/Dino/DinoLent{i}.png") for i in range(1, 12)
            ]
            self.speed = 0.80
            self.health = 150
            self.max_health = 150
            self.size = (90, 70)
        else:
            raise ValueError(f"Type de dinosaure inconnu : {self.dino_type}")

        # Redimensionner les frames d'animation
        self.animation_frames = [
            pygame.transform.scale(frame, self.size) for frame in self.animation_frames
        ]

    def random_spawn(self, side=None):
        side = side or random.choice(["left", "right", "top", "bottom"])

        map_left, map_top, map_right, map_bottom = self.map_cords
        window_left, window_top, window_right, window_bottom = 0, 0, 800, 600  # Assuming window size

        if side == "left":
            self.rect.x = window_left - self.rect.width - 10
            self.rect.y = random.randint(window_top, window_bottom - self.rect.height)
        elif side == "right":
            self.rect.x = window_right + 10
            self.rect.y = random.randint(window_top, window_bottom - self.rect.height)
        elif side == "top":
            self.rect.y = window_top - self.rect.height - 10
            self.rect.x = random.randint(window_left, window_right - self.rect.width)
        elif side == "bottom":
            self.rect.y = window_bottom + 10
            self.rect.x = random.randint(window_left, window_right - self.rect.width)

        if self.rect.x < map_left:
            self.rect.x = map_right - self.rect.width
        elif self.rect.x > map_right - self.rect.width:
            self.rect.x = map_left

        if self.rect.y < map_top:
            self.rect.y = map_bottom - self.rect.height
        elif self.rect.y > map_bottom - self.rect.height:
            self.rect.y = map_top


    def move_towards_player(self, player_rect):
        if self.rect.x < player_rect.x:
            self.rect.x += self.speed
            self.direction = "right"
        elif self.rect.x > player_rect.x:
            self.rect.x -= self.speed
            self.direction = "left"

        if self.rect.y < player_rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player_rect.y:
            self.rect.y -= self.speed

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.is_dead = True  # Le dinosaure est mort
            self.start_explosion()
        return self.is_dead

    def start_explosion(self):
        # Lance l'animation d'explosion
        self.explosion_frame = 0
        self.explosion_finished = False
        self.explosion_sound.play()  # Joue le son de l'explosion

    def animate(self):
        if self.is_dead:
            # Si le dinosaure est mort, animer l'explosion
            self.animate_explosion()
        else:
            self.current_frame += 0.2
            if self.current_frame >= len(self.animation_frames):
                self.current_frame = 0
            if self.direction == "left":
                self.image = pygame.transform.flip(self.animation_frames[int(self.current_frame)], True, False)
            else:
                self.image = self.animation_frames[int(self.current_frame)]

    def animate_explosion(self):
        # Gérer l'animation d'explosion
        if self.explosion_frame < len(self.explosion_frames):
            self.image = self.explosion_frames[self.explosion_frame]
            self.explosion_frame += 1
        else:
            self.explosion_finished = True  # Fin de l'animation d'explosion

    def draw(self, screen):
        self.animate()
        screen.blit(self.image, self.rect)

        if not self.is_dead:
            # Calcul du ratio de santé uniquement si le dinosaure est vivant
            health_ratio = self.health / self.max_health
            # Dessiner la barre de santé
            health_bar_width = 40
            health_bar_height = 4
            border_thickness = 2
            bar_x = self.rect.centerx - health_bar_width // 2
            bar_y = self.rect.y - 15

            pygame.draw.rect(screen, (50, 50, 50), (bar_x - border_thickness, bar_y - border_thickness,
                                                    health_bar_width + 2 * border_thickness,
                                                    health_bar_height + 2 * border_thickness),
                             border_radius=4)

            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, health_bar_width, health_bar_height), border_radius=4)
            pygame.draw.rect(screen, (0, 255, 0),
                             (bar_x, bar_y, int(health_bar_width * health_ratio), health_bar_height),
                             border_radius=4)

            # Ajouter un effet lumineux si la santé est faible
            if health_ratio < 0.3:
                pygame.draw.rect(screen, (255, 50, 50),
                                 (bar_x - 2, bar_y - 2, health_bar_width + 4, health_bar_height + 4),
                                 width=1, border_radius=6)

