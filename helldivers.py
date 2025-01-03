import pygame
import time

pygame.init()

# Constants 
screen = pygame.display.set_mode((480, 480),)
# screen = pygame.display.set_mode((480, 480), pygame.FULLSCREEN )

background_original = pygame.image.load("Star-Map.bmp")
background_zm_in = pygame.transform.scale(background_original.copy(), (1920, 1920))
background_zm_out = pygame.transform.scale(background_original, (480, 480))
background = background_zm_out
background_rect = background.get_rect()
background_initial_rect = background_rect.copy()

super_earth_image = pygame.image.load("super-earth.png")
super_earth_image_rect = super_earth_image.get_rect()
super_earth_image_rect.center = background_initial_rect.center

click_time = 0
dragging = False
zoomed = False
offset_x, offset_y = 0, 0
background_x, background_y = background_zm_in.get_width()//2, background_zm_in.get_height()//2

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
                offset_x = background_rect.x - event.pos[0]
                offset_y = background_rect.y - event.pos[1]

        # Mouse button up: Stop dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            # check for double click
            if time.time() - click_time < 0.3:
                if zoomed is False:
                    background = background_zm_in
                    # center background on zoom
                    background_rect.center = (-480,-480)
                elif zoomed is True: 
                    background = background_zm_out
                    # re-center all images
                    background_rect.topleft = background_initial_rect.topleft
                    super_earth_image_rect.center = background_rect.center

                # toggle zoom state
                zoomed = not zoomed
            click_time = time.time()
            dragging = False

        # Mouse motion: Update position if dragging
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                background_rect.x = event.pos[0] + offset_x
                background_rect.y = event.pos[1] + offset_y

                # Prevent the image from being dragged out of bounds
                # ({background width or height}/2) - ({image width or height}/2))
                super_earth_image_rect.x = background_rect.x + 918
                super_earth_image_rect.y = background_rect.y + 910
                
                # ({background width or height} - {screen size}), set right & bottom to left-over number ?
                if background_rect.left < -1440:
                    background_rect.left = -1440
                if background_rect.top < -1440:
                    background_rect.top = -1440
                if background_rect.right > 480:
                    background_rect.right = 480
                if background_rect.bottom > 480:
                    background_rect.bottom = 480

    screen.blit(background, background_rect)
    screen.blit(super_earth_image, super_earth_image_rect)
    pygame.display.update()

# TODO: 
# - add double click buffer time to prevent unwanted zoom level on triple clicks.
# - find way to display which faction owns what sector (API)
# - find way to optimize adding planets
# - find way to use fractal noise to fudge planet textures:
#   - use per-name-color-profiles for each planet
#   - use drop-shadows to fudge topology of planet
# - create list of planet "objects", each with multiple updatable properties. (Eventually import this data from API?)