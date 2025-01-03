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
click_time = 0
dragging = False
zoomed = False
offset_x, offset_y = 0, 0
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
            dragging = True
            offset_x = background_rect.x - event.pos[0]
            offset_y = background_rect.y - event.pos[1]

        # Mouse button up: Stop dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            if time.time() - click_time < 0.3:
                if zoomed is False:
                    print("zoomed in")
                    mouse_x, mouse_y = event.pos
                    background = pygame.transform.scale(background, (960, 960))
                    # background_rect.topleft = (background_initial_rect.x - (mouse_x - background_initial_rect.x) * 2,
                    #                            background_initial_rect.y - (mouse_y - background_initial_rect.y) * 2)
                    background_rect.center = (0,0)
                elif zoomed is True: 
                    print("zoomed out")
                    background = pygame.transform.scale(background, (480, 480))
                    background_rect.topleft = background_initial_rect.topleft
                zoomed = not zoomed
            click_time = time.time()
            dragging = False

        # Mouse motion: Update position if dragging
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                background_rect.x = event.pos[0] + offset_x
                background_rect.y = event.pos[1] + offset_y

                # Prevent the image from being dragged out of bounds
                if background_rect.left < -480:
                    background_rect.left = -480
                if background_rect.top < -480:
                    background_rect.top = -480
                if background_rect.right > 480:
                    background_rect.right = 480
                if background_rect.bottom > 480:
                    background_rect.bottom = 480

    screen.blit(background, background_rect)
    pygame.display.update()
    
pygame.quit()