import pygame
import random


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type):
        super().__init__()
        self.width = 64  # Taille de chaque tuile
        self.height = 64
        self.type = tile_type

        # Création de l'image selon le type
        self.image = pygame.Surface([self.width, self.height])
        if tile_type == 'grass':
            self.image.fill((34, 139, 34))  # Vert forêt
            self.passable = True
        elif tile_type == 'tree':
            self.image.fill((0, 100, 0))  # Vert foncé
            self.passable = False
        elif tile_type == 'water':
            self.image.fill((0, 0, 139))  # Bleu foncé
            self.passable = False
        else:  # dirt
            self.image.fill((139, 69, 19))  # Marron
            self.passable = True

        self.rect = self.image.get_rect()
        self.grid_x = x  # Position dans la grille
        self.grid_y = y
        self.update_position(0, 0)  # Position initiale à l'écran

    def update_position(self, offset_x, offset_y):
        """Met à jour la position à l'écran en fonction du décalage de la caméra"""
        self.rect.x = self.grid_x * self.width + offset_x
        self.rect.y = self.grid_y * self.height + offset_y


class World:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tile_size = 64

        # Calcul du nombre de tuiles nécessaires pour remplir l'écran +1 pour le scrolling
        self.visible_tiles_x = (screen_width // self.tile_size) + 2
        self.visible_tiles_y = (screen_height // self.tile_size) + 2

        # Dictionnaire pour stocker les tuiles
        self.tiles = {}
        # Groupe pour les tuiles actuellement visibles
        self.visible_tiles = pygame.sprite.Group()

        # Position de la première tuile visible
        self.start_x = 0
        self.start_y = 0

        # Génération initiale
        self.generate_initial_tiles()

    def generate_tile(self, x, y):
        """Génère une tuile de manière déterministe basée sur sa position"""
        if (x, y) in self.tiles:
            return self.tiles[(x, y)]

        # Utilisation des coordonnées pour générer un type de tuile de manière cohérente
        seed = (x * 73 + y * 31) % 100  # Pseudo-random mais déterministe

        if seed < 70:
            tile_type = 'grass'
        elif seed < 85:
            tile_type = 'dirt'
        elif seed < 95:
            tile_type = 'tree'
        else:
            tile_type = 'water'

        new_tile = Tile(x, y, tile_type)
        self.tiles[(x, y)] = new_tile
        return new_tile

    def generate_initial_tiles(self):
        """Génère les tuiles initiales visibles à l'écran"""
        for x in range(self.visible_tiles_x):
            for y in range(self.visible_tiles_y):
                self.generate_tile(x, y)

    def update(self, camera_x, camera_y):
        """Met à jour les positions des tuiles en fonction du mouvement de la caméra"""
        # Calcul de la position de la grille basée sur la caméra
        grid_offset_x = int(camera_x // self.tile_size)
        grid_offset_y = int(camera_y // self.tile_size)

        # Décalage pixel précis pour le rendu fluide
        pixel_offset_x = -(camera_x % self.tile_size)
        pixel_offset_y = -(camera_y % self.tile_size)

        # Mise à jour des tuiles visibles si nécessaire
        if grid_offset_x != self.start_x or grid_offset_y != self.start_y:
            self.start_x = grid_offset_x
            self.start_y = grid_offset_y
            self.update_visible_tiles()

        # Mise à jour des positions de toutes les tuiles visibles
        for tile in self.visible_tiles:
            tile.update_position(pixel_offset_x, pixel_offset_y)

    def update_visible_tiles(self):
        """Met à jour quelles tuiles sont actuellement visibles"""
        self.visible_tiles.empty()

        for x in range(self.visible_tiles_x):
            for y in range(self.visible_tiles_y):
                grid_x = self.start_x + x
                grid_y = self.start_y + y
                tile = self.generate_tile(grid_x, grid_y)
                self.visible_tiles.add(tile)

    def draw(self, screen):
        """Dessine toutes les tuiles visibles"""
        self.visible_tiles.draw(screen)

    def is_position_valid(self, x, y):
        """Vérifie si une position est valide pour le mouvement"""
        grid_x = x // self.tile_size
        grid_y = y // self.tile_size
        tile = self.tiles.get((grid_x, grid_y))
        return tile.passable if tile else True