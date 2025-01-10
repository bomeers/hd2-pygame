import time

import pygame

from functions import (load_additional_planet_data, load_planets_data_from_api,
                       log, merge_planet_data, set_planets, smoothZoom)

pygame.init()
WIDTH,HEIGHT = 480,480
screen = pygame.display.set_mode((WIDTH, HEIGHT),) # ,pygame.FULLSCREEN)

# Hide Cursor
# bitmask = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,]
# pygame.mouse.set_cursor((8, 8), (0, 0), bitmask, bitmask)


# Constants
sprite_sheet = pygame.image.load('war-table-sprite-sheet.png').convert_alpha()
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

background_original = pygame.image.load("Star-Map.bmp")
background_zm_in = pygame.transform.scale(background_original.copy(), (1920, 1920))
background_zm_out = pygame.transform.scale(background_original, (WIDTH, HEIGHT))
background = background_zm_out
background_rect = background_zm_in.get_rect()
background_initial_rect = background_rect.copy()

super_earth_sprite = pygame.Rect(335, 0, 173, 201) # (x, y, width, height)
super_earth_image = pygame.transform.scale(sprite_sheet.subsurface(super_earth_sprite), (88, 100))
super_earth_image_rect = super_earth_image.get_rect()
super_earth_image_rect.center = (WIDTH/2, HEIGHT/2)

# mars_sprite = pygame.Rect(134, 201, 67, 67) # (x, y, width, height)
# mars_image = pygame.transform.scale(sprite_sheet.subsurface(mars_sprite), (50, 50))
# mars_image_rect = mars_image.get_rect()

click_time = 0
dragging = False
zoomed = False  
offset = (0,0)
planet_offsets = []

# Get API Data
planets_data = load_planets_data_from_api("https://helldiverstrainingmanual.com/api/v1/planets")
additional_data = load_additional_planet_data("https://helldiverstrainingmanual.com/api/v1/war/status")
merged_planet_data = merge_planet_data(planets_data, additional_data)
planet_list = set_planets(merged_planet_data, sprite_location, sprite_sheet)


# Main game loop
while True:
    for event in pygame.event.get():
        # Exit the game loop when Escape is pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Mouse button down: Start dragging
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if zoomed:
                dragging = True
                offset = (background_rect.x - event.pos[0], background_rect.y - event.pos[1])
                for planet, planet_rect in planet_list:
                    planet_offset = (planet_rect.x - event.pos[0], planet_rect.y - event.pos[1])
                    planet_offsets.append(planet_offset)
            
        # Mouse button up: Stop dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            if time.time() - click_time < 0.3:
                if zoomed is False:
                    background = background_zm_in

                    currentZoom = 480
                    targetZoom = 1920
                    px = event.pos[0] / currentZoom
                    py = event.pos[1] / currentZoom # get the percentage of event X,Y to zoom from event point (not implemented yet)
                    while currentZoom < targetZoom - 3.1: # 3.1 is a buffer so that it breaks the while loop sooner
                        currentZoom = smoothZoom(currentZoom, targetZoom)
                        tempBG = pygame.transform.scale(background_original.copy(), (currentZoom, currentZoom))
                        tempRect = tempBG.get_rect()
                        screen.blit(tempBG, tempRect)
                        pygame.display.update()
                    zoomed = True

                    background_rect.center = (WIDTH/2,HEIGHT/2) # center of window size
                elif zoomed is True: 
                    background = background_zm_out
                    background_rect.topleft = background_initial_rect.topleft
                    super_earth_image_rect.center = (WIDTH/2,HEIGHT/2) # center of window size

                    currentZoom = 1920
                    targetZoom = 480
                    while currentZoom > targetZoom + 3.1:
                        currentZoom = smoothZoom(currentZoom, targetZoom)
                        tempBG = pygame.transform.scale(background_original.copy(), (currentZoom, currentZoom))
                        tempRect = tempBG.get_rect()
                        screen.blit(tempBG, tempRect)
                        pygame.display.update()
                    zoomed = False
                    
                # zoomed = not zoomed
            click_time = time.time()
            dragging = False

        # Mouse motion: Update position if dragging
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                background_rect.topleft = (event.pos[0] + offset[0], event.pos[1] + offset[1])
                
                # Prevent the image from being dragged out of bounds
                if background_rect.left < -1440: background_rect.left = -1440
                if background_rect.top < -1440: background_rect.top = -1440
                if background_rect.right > 1920: background_rect.right = 1920
                if background_rect.bottom > 1920: background_rect.bottom = 1920

                super_earth_image_rect.center = (background_rect.x + 960, background_rect.y + 960)
                # mars_image_rect.topleft = (background_rect.x + 1000, background_rect.y + 900)
                
                index = 0
                for planet, planet_rect in planet_list:
                    planet_rect.topleft = (event.pos[0] + planet_offsets[index][0], event.pos[1] + planet_offsets[index][1])
                    index = index + 1

    screen.blit(background, background_rect)
    if zoomed == True:
        for planet, planet_rect in planet_list:
            screen.blit(planet, planet_rect)
    screen.blit(super_earth_image, super_earth_image_rect)
    
    pygame.display.update()


# TODO: 
# - fix planet update position 
# - smooth zooming
# - add double click buffer time to prevent unwanted zoom level on triple clicks.
# - find way to display which faction owns what sector (API)

# API
# - use /api/v1/war/campaign to get current events and defense status