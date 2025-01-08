import pygame
import time

pygame.init()

# Constants 
screen = pygame.display.set_mode((480, 480),) # ,pygame.FULLSCREEN)

background_original = pygame.image.load("Star-Map.bmp")
background_zm_in = pygame.transform.scale(background_original.copy(), (1920, 1920))
background_zm_out = pygame.transform.scale(background_original, (480, 480))
background = background_zm_out
background_rect = background.get_rect()
background_initial_rect = background_rect.copy()

sprite_sheet = pygame.image.load('war-table-sprite-sheet.png')

super_earth_sprite = pygame.Rect(335, 0, 173, 201) # (x, y, width, height)
super_earth_image = pygame.transform.scale(sprite_sheet.subsurface(super_earth_sprite), (88, 100))
super_earth_image_rect = super_earth_image.get_rect()
super_earth_image_rect.center = background_rect.center

mars_sprite = pygame.Rect(268, 201, 67, 67) # (x, y, width, height)
mars_image = pygame.transform.scale(sprite_sheet.subsurface(mars_sprite), (50, 50))
mars_image_rect = mars_image.get_rect()

click_time = 0
dragging = False
zoomed = False  
offset = (0,0)

# hide cursor
# bitmask = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,]
# pygame.mouse.set_cursor((8, 8), (0, 0), bitmask, bitmask)


# Main game loop
while True:
    for event in pygame.event.get():
        # Exit the game loop when Escape is pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
            running = False  
            pygame.quit()
            exit()

        # Mouse button down: Start dragging
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if zoomed:
                dragging = True
                offset = (background_rect.x - event.pos[0], background_rect.y - event.pos[1])

        # Mouse button up: Stop dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            if time.time() - click_time < 0.3:
                if zoomed is False:
                    background = background_zm_in
                    background_rect.center = (-480,-480)
                elif zoomed is True: 
                    background = background_zm_out
                    background_rect.topleft = background_initial_rect.topleft
                    super_earth_image_rect.center = background_rect.center
                zoomed = not zoomed
            click_time = time.time()
            dragging = False

        # Mouse motion: Update position if dragging
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                background_rect.topleft = (event.pos[0] + offset[0], event.pos[1] + offset[1])
                
                # Prevent the image from being dragged out of bounds
                # Calculation: ({background width or height} - {screen size}), set right & bottom to left-over number ?
                if background_rect.left < -1440:
                    background_rect.left = -1440
                if background_rect.top < -1440:
                    background_rect.top = -1440
                if background_rect.right > 480:
                    background_rect.right = 480
                if background_rect.bottom > 480:
                    background_rect.bottom = 480

                # Calculation: ({background width or height}/2) - ({image width or height}/2)) EX ((480/2)-(super_earth_image_rect.x/2))
                super_earth_image_rect.topleft = (background_rect.x + 918, background_rect.y + 910)
                mars_image_rect.topleft = (background_rect.x + 1000, background_rect.y + 900)

                # PLANETS LOOP HERE
                # store planets in list of objects called "planets"
                # for i in planets:
                #   - get sprite coordinates
                #   - get x y defaults
                #   - get and set new x y coordinates

    screen.blit(background, background_rect)
    screen.blit(super_earth_image, super_earth_image_rect)
    if zoomed == True:
        screen.blit(mars_image, mars_image_rect)
    
    pygame.display.update()

# TODO: 
# - add double click buffer time to prevent unwanted zoom level on triple clicks.
# - find way to display which faction owns what sector (API)
# - create list of planet "objects", each with multiple updatable properties. (Eventually import this data from API?)
# API
# - use /api/v1/planets to get list of planets and biomes for images
# - join /api/v1/war/status by index to get x y position and player count
# - use /api/v1/war/campaign to get current events and 