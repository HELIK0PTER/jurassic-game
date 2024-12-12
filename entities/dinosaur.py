import pygame
import random


class Dinosaur:
    def __init__(self, dino_type=None):
        self.dino_type = dino_type or random.choice(["DinoNormal", "DinoRapide", "DinoLent"])
        self.configure_dinosaur()
        self.animation_frames = [pygame.transform.scale(frame, self.size) for frame in self.animation_frames]
        self.current_frame = 0
        self.image = self.animation_frames[int(self.current_frame)]
        self.rect = self.image.get_rect()
        self.random_spawn()
        self.direction = "right"

        # Initialisation pour l'explosion
        self.explosion_frames = []  # Liste des images d'explosion
        self.explosion_index = 0  # Index de l'image d'explosion actuelle
        self.explosion_timer = 0  # Timer pour gérer le délai entre les frames de l'explosion
        self.explosion_delay = 100  # Délai entre les frames d'explosion en millisecondes (100 ms)

        # Charger le son d'explosion
        self.explosion_sound = pygame.mixer.Sound("assets/sounds/Explosion.mp3")
        self.explosion_sound.set_volume(0.7)

        # Attribut pour savoir si le dinosaure est mort
        self.is_dead = False  # Initialement, le dinosaure est vivant

    def configure_dinosaur(self):
        # Configuration des caractéristiques en fonction du type de dinosaure
        if self.dino_type == "DinoNormal":
            self.animation_frames = [pygame.image.load(f"assets/images/Dino/DinoNormal{i}.png") for i in range(1, 6)]
            self.speed = 1
            self.health = 100
            self.max_health = 100
            self.size = (70, 50)
        elif self.dino_type == "DinoRapide":
            self.animation_frames = [pygame.image.load(f"assets/images/Dino/DinoRapide{i}.png") for i in range(1, 10)]
            self.speed = 2
            self.health = 25
            self.max_health = 25
            self.size = (50, 30)
        elif self.dino_type == "DinoLent":
            self.animation_frames = [pygame.image.load(f"assets/images/Dino/DinoLent{i}.png") for i in range(1, 12)]
            self.speed = 0.80
            self.health = 150
            self.max_health = 150
            self.size = (90, 70)
        else:
            raise ValueError(f"Type de dinosaure inconnu : {self.dino_type}")

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0 and not self.is_dead:
            self.is_dead = True
            self.explode()  # Appeler la fonction explode pour jouer l'explosion
        return self.health <= 0

    def explode(self):
        # Charger les images de l'explosion
        for i in range(1, 4):
            self.explosion_frames.append(pygame.image.load(f"assets/images/Dino/exploD{i}.png"))

        # Jouer le son d'explosion
        self.explosion_sound.play()

    def update_explosion(self):
        # Si l'explosion n'est pas terminée, passe à l'image suivante avec un délai
        if self.explosion_index < len(self.explosion_frames):
            self.explosion_timer += 1
            if self.explosion_timer >= self.explosion_delay:
                self.explosion_timer = 0
                self.explosion_index += 1

    def random_spawn(self):
        # Positionner le dinosaure à une position aléatoire
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            self.rect.x = -self.rect.width - 10
            self.rect.y = random.randint(0, 600)
        elif side == "right":
            self.rect.x = 800 + 10
            self.rect.y = random.randint(0, 600)
        elif side == "top":
            self.rect.x = random.randint(0, 800)
            self.rect.y = -self.rect.height - 10
        elif side == "bottom":
            self.rect.x = random.randint(0, 800)
            self.rect.y = 600 + 10

    def move_towards_player(self, player_rect):
        # Déplacer le dinosaure vers le joueur
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

    def animate(self):
        # Animation du dinosaure
        self.current_frame += 0.2
        if self.current_frame >= len(self.animation_frames):
            self.current_frame = 0
        if self.direction == "left":
            self.image = pygame.transform.flip(self.animation_frames[int(self.current_frame)], True, False)
        else:
            self.image = self.animation_frames[int(self.current_frame)]

    def draw(self, screen):
        if self.is_dead:
            # Dessiner les images d'explosion
            if self.explosion_index < len(self.explosion_frames):
                screen.blit(self.explosion_frames[self.explosion_index], self.rect)
                self.update_explosion()  # Mettre à jour l'animation de l'explosion
            return  # Ne dessine plus le dinosaure après sa mort, juste l'explosion

        self.animate()  # Met à jour l'animation avant de dessiner
        screen.blit(self.image, self.rect)

        # Dessiner la barre de santé (si vivant)
        health_bar_width = 40
        health_bar_height = 4
        border_thickness = 2
        health_ratio = self.health / self.max_health

        # Position de la barre
        bar_x = self.rect.centerx - health_bar_width // 2
        bar_y = self.rect.y - 15

        # Dessiner l'arrière-plan et bordure de la barre
        pygame.draw.rect(screen, (50, 50, 50), (bar_x - border_thickness, bar_y - border_thickness,
                                                health_bar_width + 2 * border_thickness,
                                                health_bar_height + 2 * border_thickness),
                         border_radius=4)

        # Dessiner la barre rouge (santé perdue)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, health_bar_width, health_bar_height), border_radius=4)

        # Dessiner la barre verte (santé restante)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(health_bar_width * health_ratio), health_bar_height),
                         border_radius=4)

        if health_ratio < 0.3:
            pygame.draw.rect(screen, (255, 50, 50), (bar_x - 2, bar_y - 2, health_bar_width + 4, health_bar_height + 4),
                             width=1, border_radius=6)

