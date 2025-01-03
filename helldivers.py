import pygame
import time

pygame.init()

# Constants 
screen = pygame.display.set_mode((480, 480),)
# screen = pygame.display.set_mode((480, 480), pygame.FULLSCREEN )
background = pygame.image.load("Star-Map.bmp")
background = pygame.transform.scale(background, (480, 480))
background_rect = background.get_rect()
background_initial_rect = background_rect.copy()
super_earth_image = pygame.image.load("super-earth.png")
super_earth_image_rect = super_earth_image.get_rect()
super_earth_image_rect.center = background_initial_rect.center
click_time = 0
dragging = False
zoomed = False
offset_x, offset_y = 0, 0
# hide cursor
# bitmask = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,]
# pygame.mouse.set_cursor((8, 8), (0, 0), bitmask, bitmask)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Exit the game loop when Escape is pressed
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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
                    background = pygame.transform.scale(background, (960, 960))
                    # center background on zoom
                    background_rect.center = (0,0)
                elif zoomed is True: 
                    background = pygame.transform.scale(background, (480, 480))
                    # re-center all images
                    background_rect.topleft = background_initial_rect.topleft
                    super_earth_image_rect.center = background_initial_rect.center

                # toggle zoom state
                zoomed = not zoomed
            click_time = time.time()
            dragging = False

        # Mouse motion: Update position if dragging
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                background_rect.x = event.pos[0] + offset_x
                background_rect.y = event.pos[1] + offset_y
                super_earth_image_rect.x = background_rect.x + 437.5
                super_earth_image_rect.y = background_rect.y + 430
                
                # Prevent the image from being dragged out of bounds
                if background_rect.left < -480:
                    background_rect.left = -480
                if background_rect.top < -480:
                    background_rect.top = -480
                if background_rect.right > 480:
                    background_rect.right = 480
                if background_rect.bottom > 480:
                    background_rect.bottom = 480

                # to rescale super earth, use: ({background-width-or-height}/2) + ({image-width-or-height}/2)
                if super_earth_image_rect.left < -42.5:
                    super_earth_image_rect.left = -42.5
                if super_earth_image_rect.top < -50:
                    super_earth_image_rect.top = -50
                if super_earth_image_rect.right > 522.5:
                    super_earth_image_rect.right = 522.5
                if super_earth_image_rect.bottom > 530:
                    super_earth_image_rect.bottom = 530

    screen.blit(background, background_rect)
    screen.blit(super_earth_image, super_earth_image_rect)
    pygame.display.update()
    
pygame.quit()

# TODO: 
# - zoom in further just like in game table
# - update super earth zoom level and boundaries
# TODO STRETCH: 
# - find way to display which faction owns what sector 
# - find way to optimize adding planets
# - find way to use fractal noise to fudge planet textures:
#   - use per-name-color-profiles for each planet
#   - use drop-shadows to fudge topology of planet
# - create list of planet "objects", each with multiple updatable properties. (Eventually import this data from API?)