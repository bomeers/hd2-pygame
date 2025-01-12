import pygame
import random
from pygame.locals import *
from functions import (load_additional_planet_data, load_planets_data_from_api, log, merge_planet_data, set_planets, smoothZoom)

pygame.init()

# Screen setup
screen_width = 480
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Helldivers War Table")

# Load images
background = pygame.image.load('Star-Map.bmp').convert()
sprite_sheet = pygame.image.load('war-table-sprite-sheet.png').convert_alpha()  # Using convert_alpha to support transparency
sprite_location = {
        "toxic": (0, 0, 67, 67),
        "morass": (67, 0, 67, 67),
        "desert": (134, 0, 67, 67),
        "canyon": (201, 0, 67, 67),
        "mesa": (268, 0, 67, 67),
        "highlands": (0, 67, 67, 67),
        "rainforest": (67, 67, 67, 67),
        "jungle": (134, 67, 67, 67),
        "ethereal": (201, 67, 67, 67),
        "crimsonmoor": (268, 67, 67, 67),
        "icemoss": (0, 134, 67, 67),
        "winter": (67, 134, 67, 67),
        "tundra": (134, 134, 67, 67),
        "desolate": (201, 134, 67, 67),
        "swamp": (268, 134, 67, 67),
        "moon": (0, 201, 67, 67),
        "blackhole": (67, 201, 67, 67),
        "mars": (134, 201, 67, 67),
        "undergrowth": (67, 0, 67, 67),         # same as morass
        "icemoss-special": (0, 134, 67, 67),    # same as icemoss
        "No Biome": (0, 0, 67, 67),
    }

super_earth_sprite = pygame.Rect(335, 0, 173, 201) # (x, y, width, height)
super_earth_image = pygame.transform.scale(sprite_sheet.subsurface(super_earth_sprite), (88, 100))
super_earth_image_rect = super_earth_image.get_rect()
super_earth_image_rect.center = (screen_width/2, screen_height/2)

# Load planet data from the API
planets_data = load_planets_data_from_api("https://helldiverstrainingmanual.com/api/v1/planets")
additional_data = load_additional_planet_data("https://helldiverstrainingmanual.com/api/v1/war/status")
merged_planet_data = merge_planet_data(planets_data, additional_data)
planet_list = set_planets(merged_planet_data, sprite_location, sprite_sheet)


# /////////
# Classes /
# /////////
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)  # Initial camera position
        self.world_size = (width * 2, height * 2)  # World size (example: double the size of the window)
        self.window_size = (width, height)  # Window size
        self.dragging = False  # To track if the user is dragging the camera
        self.drag_start_pos = None  # Start position of the drag
        self.zoom_default = 4
        self.zoom_level = 0.5  # Default zoom level (1 = zoomed-in)


    def apply(self, entity):
        """Moves the entity based on camera position."""
        # Scale entity position based on zoom level
        return entity.rect.move(self.camera.topleft).inflate(entity.rect.width * (self.zoom_level - self.zoom_default), entity.rect.height * (self.zoom_level - self.zoom_default))

    def start_drag(self, pos):
        """Initiates dragging when mouse is pressed."""
        if self.zoom_level == self.zoom_default:  # Only allow dragging when zoomed in
            self.dragging = True
            self.drag_start_pos = pos

    def stop_drag(self):
        """Stops dragging when mouse is released."""
        self.dragging = False

    def drag(self, pos):
        """Update camera position based on drag movement."""
        if self.zoom_level == self.zoom_default and self.dragging:  # Only allow dragging when zoomed in
            dx = pos[0] - self.drag_start_pos[0]
            dy = pos[1] - self.drag_start_pos[1]
            self.camera.x += dx
            self.camera.y += dy
            self.drag_start_pos = pos  # Update the drag start position

    def toggle_zoom(self):
        """Toggle between two zoom levels: zoomed-in and zoomed-out."""
        if self.zoom_level == self.zoom_default:
            self.zoom_level = 0.5  # Zoomed out
            self.camera.topleft = (0, 0)  # Reset camera position
        else:
            self.zoom_level = self.zoom_default  # Zoomed in
            self.camera.topleft = (-1977, -1977) # Set camera position to the center of the world CHANGE THIS TO SET BACKGROUND POS INSTEAD

class Planet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = sprite_sheet
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# ///////////
# Constants /
# ///////////
clock = pygame.time.Clock()
camera = Camera(screen_width, screen_height)
planets = pygame.sprite.Group()

# Place 5 planets randomly on the map
for _ in range(10):
    x = random.randint(0, 1080)  # Random x position within the world size
    y = random.randint(0, 1080)  # Random y position within the world size
    planet = Planet(x, y)
    planets.add(planet)

last_click_time = 0
initial_center = False


# ///////////
# Game loop /
# ///////////
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
            pygame.quit() # Exit the game loop when Escape is pressed
            exit()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button pressed
                current_time = pygame.time.get_ticks()
                if current_time - last_click_time <= 300:
                    camera.toggle_zoom()
                last_click_time = current_time
                camera.start_drag(event.pos)  # Start dragging

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button released
                camera.stop_drag()

    if camera.dragging:
        mouse_pos = pygame.mouse.get_pos() # update the camera's position
        camera.drag(mouse_pos)
    
    # Apply the camera movement to the background (parallax)
    background_offset_x = camera.camera.x * 0.85 
    background_offset_y = camera.camera.y * 0.85
    
    # Scale the backgrounds based on zoom level
    scaled_background = pygame.transform.scale(background, (int(background.get_width() * camera.zoom_level), int(background.get_height() * camera.zoom_level)))

    # Draw the background
    background_rect = pygame.Rect(background_offset_x, background_offset_y, *scaled_background.get_size())
    if initial_center == False:
        background_rect.center = (screen_width/2, screen_height/2)
        initial_center = True
    screen.blit(scaled_background, background_rect)

    super_earth_image_rect.center = background_rect.center
    screen.blit(super_earth_image, super_earth_image_rect)

    # Draw the planets 
    for planet in planets:
        screen.blit(planet.image, camera.apply(planet))

    pygame.display.update() # Update the display

    clock.tick(60) # Set the FPS

# add back in the 2nd parallax background layer then make one not have acceleration