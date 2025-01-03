import pygame
import time

pygame.init()

# Constants 
# screen = pygame.display.set_mode((480, 480), pygame.FULLSCREEN )
screen = pygame.display.set_mode((480, 480),)
background = pygame.image.load("Star-Map.bmp")
background_zoomed_out = pygame.transform.scale(background, (480, 480))
background_rect = background.get_rect()
click_time = 0
dragging = False
zoomed = False
offset_x, offset_y = 0, 0
bitmask = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,]
pygame.mouse.set_cursor((8, 8), (0, 0), bitmask, bitmask)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Exit the game loop when Escape is pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False  
            pygame.quit()
            exit()

         # Mouse button down: Start dragging
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if background_rect.collidepoint(event.pos):  # Check if mouse is over the image
                dragging = True
                # Calculate offset
                offset_x = background_rect.x - event.pos[0]
                offset_y = background_rect.y - event.pos[1]

        # Mouse button up: Stop dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            if time.time() - click_time < 0.3:
                print("double click")
                if zoomed is True:
                    background = pygame.transform.scale(background, (960, 960))
                elif zoomed is False: 
                    background = pygame.transform.scale(background, (480, 480))
                zoomed = not zoomed
            click_time = time.time()
            dragging = False

        # Mouse motion: Update position if dragging
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                background_rect.x = event.pos[0] + offset_x
                background_rect.y = event.pos[1] + offset_y

    screen.blit(background, background_rect)
    pygame.display.update()
    
pygame.quit()





# running = True
# while running:
#     for event in pygame.event.get():
#         # Mouse button events for dragging and zooming
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 1:  # Left mouse button for zoom in/out and drag
#                 current_time = pygame.time.get_ticks()
                
#                 # Check for double-click (within DOUBLE_CLICK_TIME milliseconds)
#                 if current_time - last_click_time <= DOUBLE_CLICK_TIME:
#                     double_click = True
#                 else:
#                     double_click = False

#                 last_click_time = current_time  # Update the last click time
                
#                 # If it's a double-click, zoom in or out
#                 if double_click:
#                     if zoomed_in:
#                         # Zoom out
#                         zoom_level /= ZOOM_FACTOR
#                         # Update the zoomed-in image if needed
#                         zoomed_in = False
#                     else:
#                         # Zoom in
#                         zoom_level *= ZOOM_FACTOR
#                         # Resize the zoomed-in image to match the new zoom level and store its rect
#                         zoomed_in_image_scaled = resize_image(zoomed_in_image, image_rect.width, image_rect.height)
#                         zoomed_in_rect = zoomed_in_image_scaled.get_rect(center=image_rect.center)
#                         zoomed_in_image = zoomed_in_image_scaled
#                         zoomed_in = True

#                     # Update the zoom state
#                     image = pygame.image.load(image_path)  # Reload the background image
#                     image = resize_image(image, WIDTH * zoom_level, HEIGHT * zoom_level)
#                     image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

#                 # Start dragging
#                 if not double_click:  # Don't start dragging if it's a double-click
#                     if image_rect.collidepoint(event.pos):
#                         dragging = True
#                         offset_x = image_rect.x - event.pos[0]
#                         offset_y = image_rect.y - event.pos[1]

#         elif event.type == pygame.MOUSEBUTTONUP:
#             dragging = False

#         # Mouse motion event for dragging the image
#         if event.type == pygame.MOUSEMOTION:
#             if dragging:
#                 # Update image position while ensuring it doesn't go out of bounds
#                 image_rect.x = event.pos[0] + offset_x
#                 image_rect.y = event.pos[1] + offset_y

#                 # Prevent the image from being dragged out of bounds
#                 if image_rect.left > 0:
#                     image_rect.left = 0
#                 if image_rect.top > 0:
#                     image_rect.top = 0
#                 if image_rect.right < WIDTH:
#                     image_rect.right = WIDTH
#                 if image_rect.bottom < HEIGHT:
#                     image_rect.bottom = HEIGHT)

#     # Clear the screen with a black background
#     screen.fill((0, 0, 0))  # Black background

#     # Draw the background image (Star-Map.bmp) which is always visible
#     screen.blit(image, image_rect)
    
#     # If zoomed out, draw the zoomed-out image
#     if not zoomed_in:
#         screen.blit(zoomed_out_image, zoomed_out_rect)

#     # If zoomed in, draw the zoomed-in image (already resized) on top
#     if zoomed_in:
#         screen.blit(zoomed_in_image, zoomed_in_rect)
#
#    # Update the screen
#    pygame.display.flip()

# # Quit Pygame
# pygame.quit()
