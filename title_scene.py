import pygame
from scene import Scene

class TitleScene(Scene):
    def __init__(self, logo_surface, logo_rect, sky_surface, ground_surface, ground_tiles):
        self.logo_surface = logo_surface
        self.logo_rect = logo_rect
        self.font = pygame.font.Font('resources/font/NES.otf', 32)
        self.sky_surface = sky_surface
        self.ground_surface = ground_surface
        self.ground_tiles = ground_tiles

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "game"
        return None

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.sky_surface, (0, 0))
        for ground_rect in self.ground_tiles:
            screen.blit(self.ground_surface, ground_rect.topleft)
        screen.blit(self.logo_surface, self.logo_rect)
        # Create the "Press ENTER to Start" text
        text = self.font.render("Press ENTER to Start", False, (255, 255, 255))

        # Get the rect of the text and center it on the screen
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        # Blit the centered text to the screen
        screen.blit(text, text_rect)
        