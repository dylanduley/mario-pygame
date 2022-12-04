import pygame
from sys import exit
from settings import *
from player import Player

# Initialize Pygame
pygame.init()

# Set up the display
def setup_display():
    screen = pygame.display.set_mode((wScreen, hScreen))
    pygame.display.set_caption('Super Mario Bros. Alpha 0.1')
    return screen

# Load assets
def load_assets():
    # Load and scale the sky surface
    sky_surface = pygame.image.load('resources/graphics/background.png').convert()
    sky_surface = pygame.transform.scale(sky_surface, (wScreen, hScreen))

    # Load the logo surface
    logo_surface = pygame.image.load('resources/graphics/logo.png').convert()

    # Original dimensions
    original_width, original_height = 176, 87

    # Desired size (increased size factor)
    size_factor = 1.1  # You can adjust this factor to make it bigger or smaller
    desired_width = int(wScreen * 0.6 * size_factor)
    desired_height = int(hScreen * 0.3 * size_factor)

    # Calculate the aspect ratio
    aspect_ratio = original_width / original_height

    # Calculate new dimensions while maintaining aspect ratio
    if (desired_width / desired_height) > aspect_ratio:
        new_width = desired_height * aspect_ratio
        new_height = desired_height
    else:
        new_width = desired_width
        new_height = desired_width / aspect_ratio

    # Scale the logo surface
    logo_surface = pygame.transform.scale(logo_surface, (int(new_width), int(new_height)))

    # Get the rectangle for centering
    logo_rect = logo_surface.get_rect(center=(wScreen / 2, hScreen / 4))

    # Load and scale the ground surface
    ground_surface = pygame.image.load('resources/graphics/groundBlock.png').convert()
    ground_surface = pygame.transform.scale(ground_surface, (sprite_size, sprite_size))

    return sky_surface, logo_surface, logo_rect, ground_surface

# Create ground tiles
def create_ground_tiles(ground_surface):
    ground_tiles = []
    for i in range(round(wGrid)):
        ground_rect = ground_surface.get_rect(topleft=(i * sprite_size, hScreen - sprite_size))
        ground_tiles.append(ground_rect)
    return ground_tiles

# Load sounds
def load_sounds():
    bg_music = pygame.mixer.Sound('resources/sound/overworld_theme.ogg')
    bg_music.play(loops=-1)

    jump_sound = pygame.mixer.Sound('resources/sound/small_jump.ogg')
    jump_sound.set_volume(0.5)

    return jump_sound

# Main game loop
def main():
    screen = setup_display()
    sky_surface, logo_surface, logo_rect, ground_surface = load_assets()
    ground_tiles = create_ground_tiles(ground_surface)
    jump_sound = load_sounds()

    player1 = Player(sprite_size)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Draw background
        screen.blit(sky_surface, (0, 0))

        # Draw ground tiles
        for ground_rect in ground_tiles:
            screen.blit(ground_surface, ground_rect.topleft)

        # Draw logo
        screen.blit(logo_surface, logo_rect.topleft)

        # Use the first ground tile as ground_rect for player movement and gravity
        ground_rect = ground_tiles[0]  # Assuming the player interacts with the first ground tile

        # Player actions
        player1.player_movement(ground_rect, jump_sound)
        player1.player_jump_gravity(ground_rect)
        player1.player_animation(ground_rect)

        # Draw player
        screen.blit(player1.player_surf, player1.player_rect)

        # Update the display and set the frame rate
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
