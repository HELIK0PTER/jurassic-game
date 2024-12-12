import pygame
import random
from core.states.state import State
from entities.player import Player
from entities.dinosaur import Dinosaur

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600

class Gameplay(State):
    def __init__(self, player_name=""):
        super().__init__()
        self.player = Player(375, 275)
        self.enemies = []
        self.spawn_timer = 0
        self.player_name = player_name
        self.score = 0
        self.font = pygame.font.Font(None, 36)

        # Chargement des images pour le décor infini
        self.rock_image = pygame.image.load("assets/images/rock.png")
        self.tree_image = pygame.image.load("assets/images/tree.png")
        self.hole_image = pygame.image.load("assets/images/hole.png")

        # Liste d'éléments de décor
        self.decor_elements = []
        self.decor_speed = 5  # Vitesse de défilement du décor

        # Initialisation audio
        pygame.mixer.init()

        # Charger la musique de fond
        pygame.mixer.music.load("assets/sounds/background_song.mp3")
        pygame.mixer.music.play(-1)  # Jouer en boucle
        self.background_music = pygame.mixer.music  # Référence à la musique de fond

        # Charger les sons
        self.shoot_sound = pygame.mixer.Sound("assets/sounds/pistolet.ogg")
        self.shoot_sound.set_volume(0.7)  # Volume normal pour les sons de tir (entre 0 et 1)

        self.create_decor()

    def create_decor(self):
        """Crée le décor infini avec des éléments comme des rochers, arbres et trous."""
        x_pos = 0
        while x_pos < WIDTH:
            # Ajouter des éléments de décor à des positions x successives
            self.decor_elements.append({
                'type': random.choice(['rock', 'tree', 'hole']),
                'x': x_pos,
                'y': random.randint(350, 450),  # Position verticale aléatoire
                'image': None
            })
            x_pos += random.choice([100, 150, 200])  # Espacement aléatoire entre les éléments

        # Assigner les images aux éléments du décor
        for element in self.decor_elements:
            if element['type'] == 'rock':
                element['image'] = self.rock_image
            elif element['type'] == 'tree':
                element['image'] = self.tree_image
            elif element['type'] == 'hole':
                element['image'] = self.hole_image

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        mouse_pos = pygame.mouse.get_pos()
        if keys[pygame.K_SPACE]:
            self.player.shoot(mouse_pos, self.shoot_sound)

    def update(self):
        # Déplacer les éléments du décor à gauche
        for element in self.decor_elements:
            element['x'] -= self.decor_speed
            # Repositionner les éléments qui sortent de l'écran à droite
            if element['x'] < -element['image'].get_width():
                element['x'] = WIDTH
                element['y'] = random.randint(350, 450)

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
                self.next_state = "GAMEOVER"
                return  # Arrêter le reste de l'exécution de cette frame

        # Mettre à jour le score tous les 60 ticks
        if pygame.time.get_ticks() % 60 == 0:
            self.add_score(1)

    def render(self, screen):
        screen.fill((0, 0, 0))  # Fond noir

        # Afficher les éléments du décor
        for element in self.decor_elements:
            screen.blit(element['image'], (element['x'], element['y']))

        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)

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
