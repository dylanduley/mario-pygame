import pygame
from scene import Scene
from player import Player
from settings import wScreen, hScreen

class GameScene(Scene):
    def __init__(self, sprite_size, ground_surface, ground_tiles, jump_sound):
        self.player = Player(sprite_size)
        self.ground_surface = ground_surface
        self.ground_tiles = ground_tiles
        self.jump_sound = jump_sound
        self.sky_surface = pygame.image.load('resources/graphics/background.png').convert()
        self.sky_surface = pygame.transform.scale(self.sky_surface, (wScreen, hScreen))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "title"
        return None

    def update(self):
        ground_rect = self.ground_tiles[0]
        self.player.player_movement(ground_rect, self.jump_sound)
        self.player.player_jump_gravity(ground_rect)
        self.player.player_animation(ground_rect)

    def draw(self, screen):
        screen.blit(self.sky_surface, (0, 0))
        for ground_rect in self.ground_tiles:
            screen.blit(self.ground_surface, ground_rect.topleft)
        screen.blit(self.player.player_surf, self.player.player_rect)