import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SPRITE_LOCATION
from classes import Camera, Planet
from functions import load_planet_data, smoothZoom

# Setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Helldivers War Table")


# Fonts
font = pygame.font.Font(None, 12)  # Set up font for planet names

# Images
background = pygame.image.load('images/Star-Map-original.bmp').convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2))
sectors = pygame.image.load('images/sectors.png').convert_alpha()
sectors.set_alpha(25)
sprite_sheet = pygame.image.load('images/war-table-sprite-sheet.png').convert_alpha()  # Using convert_alpha to support transparency

super_earth_image = pygame.transform.scale(sprite_sheet.subsurface(pygame.Rect(335, 0, 173, 201)), (88, 100))
super_earth_image.get_rect().center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

clock = pygame.time.Clock()
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

# Load and set planet data
planets_data = load_planet_data(sprite_sheet)
planets = pygame.sprite.Group()
for planet in planets_data:
    item = Planet(
        planet['index'], 
        planet['name'], 
        planet['sector'], 
        planet['biome'], 
        planet['owner'], 
        planet['health'], 
        planet['regenPerSecond'], 
        planet['players'], 
        (planet["position"]["x"] - -1.0) * (SCREEN_HEIGHT * 2) / (1.0 - -1.0), 
        (-(planet["position"]["y"]) - -1.0) * (SCREEN_HEIGHT * 2) / (1.0 - -1.0),
        pygame.transform.scale(sprite_sheet.subsurface(pygame.Rect(SPRITE_LOCATION[planet['biome']])), (20, 20)))
    planets.add(item)


# Game loop 
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
            pygame.quit()
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
        planet.draw(screen, camera, font)

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