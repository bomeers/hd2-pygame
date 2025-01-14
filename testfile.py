import pygame
# from pygame.locals import *
from functions import (load_planet_data, smoothZoom)

pygame.init()

screen_width, screen_height = 480, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Helldivers War Table")


# ////////
# Images /
# ////////
background = pygame.image.load('Star-Map-original.bmp').convert()
background = pygame.transform.scale(background, (screen_width * 2, screen_height * 2))
sectors = pygame.image.load('sectors.png').convert_alpha()
sectors.set_alpha(25)
sprite_sheet = pygame.image.load('war-table-sprite-sheet.png').convert_alpha()  # Using convert_alpha to support transparency

super_earth_image = pygame.transform.scale(sprite_sheet.subsurface(pygame.Rect(335, 0, 173, 201)), (88, 100))
super_earth_image.get_rect().center = (screen_width/2, screen_height/2)

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
        self.camera.center = (0,0)
        # self.zoom_default = 4
        # self.zoom_level = 0.5  # Default zoom level (1 = zoomed-in)

    def apply(self, entity):
        """Moves the entity based on camera position."""
        return entity.rect.move(self.camera.topleft)

    def start_drag(self, pos):
        """Initiates dragging when mouse is pressed."""
        self.dragging = True
        self.drag_start_pos = pos

    def stop_drag(self):
        """Stops dragging when mouse is released."""
        self.dragging = False

    def drag(self, pos):
        """Update camera position based on drag movement."""
        if self.dragging:  # Only allow dragging when zoomed in
            dx = pos[0] - self.drag_start_pos[0]
            dy = pos[1] - self.drag_start_pos[1]
            self.camera.x += dx
            self.camera.y += dy
            self.drag_start_pos = pos  # Update the drag start position

            self.camera.x = max(-480, min(self.camera.x, 0))
            self.camera.y = max(-480, min(self.camera.y, 0))

class Planet(pygame.sprite.Sprite):
    def __init__(self, index, name, sector, biome, owner, health, regenPerSecond, players, x, y):
        super().__init__()
        self.index = index
        self.name = name
        self.sector = sector
        self.biome = biome
        self.owner = owner
        self.health = health
        self.regenPerSecond = regenPerSecond
        self.players = players
        self.image = pygame.transform.scale(sprite_sheet.subsurface(pygame.Rect(sprite_location[biome])), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# ///////////
# Constants /
# ///////////
clock = pygame.time.Clock()
camera = Camera(screen_width, screen_height)

# Load planet data from the API
planets_data = load_planet_data(sprite_sheet)

planets = pygame.sprite.Group()
for planet in planets_data:
    x = (planet["position"]["x"] - -1.0) * (screen_height * 2) / (1.0 - -1.0)
    y = (-(planet["position"]["y"]) - -1.0) * (screen_height * 2) / (1.0 - -1.0)
    item = Planet(planet['index'], planet['name'], planet['sector'], planet['biome'], planet['owner'], planet['health'], planet['regenPerSecond'], planet['players'], x, y)
    planets.add(item)


# ///////////
# Game loop /
# ///////////
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
            pygame.quit() # Exit the game loop when Escape is pressed
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            camera.start_drag(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            camera.stop_drag()
        elif event.type == pygame.MOUSEMOTION:
            camera.drag(event.pos)
    
    
    # Draw scene
    screen.blit(background, (camera.camera.x/1.2, camera.camera.y/1.2))
    screen.blit(sectors, (camera.camera.x, camera.camera.y))

    for planet in planets:
        screen.blit(planet.image, camera.apply(planet))

    screen.blit(super_earth_image, (camera.camera.x + 435, camera.camera.y + 440)) # not sure what the equasion is yet


    pygame.display.update()
    clock.tick(60) # Set the FPS

# TODO: 
# - RE-ADD ZOOM FUNCTIONALITY LAST (removed for now to reduce logic stress)
# - add smooth zooming to camera
# - add double click buffer time to prevent unwanted zoom level on triple clicks.
# - find way to display which faction owns what sector (API)

# API
# - use /api/v1/war/campaign to get current events and defense status