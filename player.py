import pygame

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_size):
        super().__init__()
        self.sprite_size = sprite_size
        self.images = {
            "stand": self.load_and_scale('resources/graphics/Player/player_stand.png'),
            "walk_1": self.load_and_scale('resources/graphics/Player/player_walk_1.png'),
            "walk_2": self.load_and_scale('resources/graphics/Player/player_walk_2.png'),
            "walk_slide": self.load_and_scale('resources/graphics/Player/player_walk_slide.png'),
            "jump": self.load_and_scale('resources/graphics/Player/player_jump.png'),
        }
        self.player_walk = [self.images["walk_1"], self.images["walk_2"]]
        self.player_index = 0
        self.player_direction = 0
        self.player_surf = self.images["stand"]
        self.player_rect = self.player_surf.get_rect(bottomleft=(96, 624))
        self.player_gravity = 0
        self.player_speed = 0
        self.deceleration = 0.4  # Increased deceleration
        self.base_max_speed = 5  # Default maximum speed
        self.boosted_max_speed = 8  # Boosted maximum speed
        self.acceleration = 0.8  # Increased acceleration
        self.sliding = False  # To control slide animation

    def load_and_scale(self, image_path):
        image = pygame.image.load(image_path).convert_alpha()
        return pygame.transform.scale(image, (self.sprite_size, self.sprite_size))

    def player_animation(self, ground_rect):
        # Player is above ground
        if self.player_rect.bottom < ground_rect.top:
            self.player_surf = self.images["jump"]
            if self.player_direction == 1:
                self.player_surf = pygame.transform.flip(self.player_surf, True, False)
        # Player is sliding
        elif self.sliding:
            self.player_surf = self.images["walk_slide"]
            if self.player_direction == 0:
                self.player_surf = pygame.transform.flip(self.player_surf, True, False)  # Flip for left direction
        # Player is moving forward
        elif self.player_speed > 0:
            self.player_index += 0.2
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.player_surf = self.player_walk[int(self.player_index)]
            self.player_direction = 0
            self.sliding = False  # Reset sliding state
        # Player is moving backward
        elif self.player_speed < 0:
            self.player_index += 0.2
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.player_surf = self.player_walk[int(self.player_index)]
            self.player_surf = pygame.transform.flip(self.player_surf, True, False)
            self.player_direction = 1
            self.sliding = False  # Reset sliding state
        # Player is Standing
        else:
            self.player_surf = self.images["stand"]
            if self.player_direction == 1:
                self.player_surf = pygame.transform.flip(self.player_surf, True, False)

    def player_movement(self, ground_rect, jump_sound):
        key_down = pygame.key.get_pressed()
        # Key down press set to K for moving faster
        max_speed = self.boosted_max_speed if key_down[pygame.K_x] else self.base_max_speed

        if key_down[pygame.K_LEFT]:
            if self.player_speed > 0:  # If currently moving right, slide before changing direction
                self.sliding = True
                self.player_speed -= self.deceleration * 2  # Rapid deceleration
                if self.player_speed < 0:  # Ensure speed doesn't go negative
                    self.player_speed = 0
            else:
                if self.player_speed > -max_speed:
                    self.player_speed += -self.acceleration
                self.sliding = False  # Reset sliding state

        elif key_down[pygame.K_RIGHT]:
            if self.player_speed < 0:  # If currently moving left, slide before changing direction
                self.sliding = True
                self.player_speed += self.deceleration * 2  # Rapid deceleration
                if self.player_speed > 0:  # Ensure speed doesn't go positive
                    self.player_speed = 0
            else:
                if self.player_speed < max_speed:
                    self.player_speed += self.acceleration
                self.sliding = False  # Reset sliding state

        else:
            # Decelerate when no keys are pressed
            if self.player_speed > 0:
                self.player_speed -= self.deceleration
                if self.player_speed < 0:
                    self.player_speed = 0
            elif self.player_speed < 0:
                self.player_speed += self.deceleration
                if self.player_speed > 0:
                    self.player_speed = 0

        self.player_rect.x += self.player_speed

        if key_down[pygame.K_SPACE] and self.player_rect.bottom == ground_rect.top:
            self.player_gravity = -20
            jump_sound.play()

    def player_jump_gravity(self, ground_rect):
        self.player_gravity += 1
        self.player_rect.y += self.player_gravity
        # Check that Player is above ground and adjusts accordingly
        if self.player_rect.bottom >= ground_rect.top:
            self.player_rect.bottom = ground_rect.top

class Player:
    def __init__(self, sprite_size):
        self.player_sprite = PlayerSprite(sprite_size)

    def player_animation(self, ground_rect):
        # Call the animation method with only ground_rect
        self.player_sprite.player_animation(ground_rect)

    def player_movement(self, ground_rect, jump_sound):
        self.player_sprite.player_movement(ground_rect, jump_sound)

    def player_jump_gravity(self, ground_rect):
        self.player_sprite.player_jump_gravity(ground_rect)

    @property
    def player_surf(self):
        return self.player_sprite.player_surf

    @property
    def player_rect(self):
        return self.player_sprite.player_rect
