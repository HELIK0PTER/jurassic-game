import pygame
import random


class Dinosaur:
    def __init__(self, dino_type=None):
        """
        Initialise un dinosaure en fonction de son type.
        Si aucun type n'est spécifié, un type est choisi aléatoirement.
        """
        # Choisir un type de dinosaure aléatoire si aucun n'est fourni
        self.dino_type = dino_type or random.choice(["DinoNormal", "DinoRapide", "DinoLent"])

        # Configurer les caractéristiques en fonction du type de dinosaure
        self.configure_dinosaur()

        # Redimensionner les frames pour correspondre à la taille
        self.animation_frames = [
            pygame.transform.scale(frame, self.size) for frame in self.animation_frames
        ]

        # Initialisation des propriétés d'animation et de position
        self.current_frame = 0
        self.image = self.animation_frames[int(self.current_frame)]
        self.rect = self.image.get_rect()
        self.random_spawn()
        self.direction = "right"

    def configure_dinosaur(self):
        """
        Configure les caractéristiques et animations en fonction du type de dinosaure.
        """
        if self.dino_type == "DinoNormal":
            self.animation_frames = [
                pygame.image.load(f"assets/images/Dino/DinoNormal{i}.png") for i in range(1, 6)
            ]
            self.speed = 1
            self.health = 100
            self.max_health = 100
            self.size = (70, 50)  # Taille normale
        elif self.dino_type == "DinoRapide":
            self.animation_frames = [
                pygame.image.load(f"assets/images/Dino/DinoRapide{i}.png") for i in range(1, 10)
            ]
            self.speed = 2
            self.health = 25
            self.max_health = 25
            self.size = (50, 30)  # Taille petite
        elif self.dino_type == "DinoLent":
            self.animation_frames = [
                pygame.image.load(f"assets/images/Dino/DinoLent{i}.png") for i in range(1, 12)
            ]
            self.speed = 0.80
            self.health = 150
            self.max_health = 150
            self.size = (90, 70)  # Taille grande
        else:
            raise ValueError(f"Type de dinosaure inconnu : {self.dino_type}")

    def random_spawn(self):
        """
        Positionne le dinosaure à une position aléatoire en dehors de l'écran.
        """
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
        """
        Déplace le dinosaure vers le joueur et ajuste la direction.
        """
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
        """
        Inflige des dégâts au dinosaure. Retourne True si le dinosaure est détruit.
        """
        self.health -= amount
        return self.health <= 0

    def animate(self):
        """
        Met à jour l'image du dinosaure pour créer une animation.
        """
        self.current_frame += 0.2  # Change de frame progressivement
        if self.current_frame >= len(self.animation_frames):
            self.current_frame = 0  # Boucle sur les frames

        # Choix de l'image en fonction de la direction
        if self.direction == "left":
            self.image = pygame.transform.flip(self.animation_frames[int(self.current_frame)], True, False)
        else:
            self.image = self.animation_frames[int(self.current_frame)]

    def draw(self, screen):
        """
        Dessine le dinosaure et sa barre de santé.
        """
        self.animate()  # Met à jour l'animation avant de dessiner
        screen.blit(self.image, self.rect)

        # Dessiner la barre de santé
        health_bar_width = 40
        health_bar_height = 4
        border_thickness = 2
        health_ratio = self.health / self.max_health

        # Position de la barre
        bar_x = self.rect.centerx - health_bar_width // 2
        bar_y = self.rect.y - 15

        # Dessiner l'arrière-plan et bordure de la barre
        pygame.draw.rect(screen, (50, 50, 50), (bar_x - border_thickness, bar_y - border_thickness,
                                                health_bar_width + 2 * border_thickness, health_bar_height + 2 * border_thickness),
                         border_radius=4)

        # Dessiner la barre rouge (santé perdue)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, health_bar_width, health_bar_height), border_radius=4)

        # Dessiner la barre verte (santé restante)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(health_bar_width * health_ratio), health_bar_height),
                         border_radius=4)

        # Ajout d'une légère lueur autour (effet esthétique)
        if health_ratio < 0.3:
            pygame.draw.rect(screen, (255, 50, 50), (bar_x - 2, bar_y - 2, health_bar_width + 4, health_bar_height + 4),
                             width=1, border_radius=6)