import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Click and Drag Camera with Ants and Parallax")

# Load the background images (dirt.jpeg as the main background and a distant layer)
background = pygame.image.load('Star-Map.bmp').convert()
# Create a distant background image (e.g., mountains or sky)
distant_background = pygame.image.load('Star-Map.bmp').convert()

# Load the ant image (ant.png)
ant_image = pygame.image.load('war-table-sprite-sheet.png').convert_alpha()  # Using convert_alpha to support transparency

# Create the Camera class
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)  # Initial camera position
        self.world_size = (width * 2, height * 2)  # World size (example: double the size of the window)
        self.window_size = (width, height)  # Window size
        self.dragging = False  # To track if the user is dragging the camera
        self.drag_start_pos = None  # Start position of the drag

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
        if self.dragging:
            dx = pos[0] - self.drag_start_pos[0]
            dy = pos[1] - self.drag_start_pos[1]
            self.camera.x += dx
            self.camera.y += dy
            self.drag_start_pos = pos  # Update the drag start position

# Create the Ant class
class Ant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = ant_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Game loop
running = True
clock = pygame.time.Clock()

camera = Camera(screen_width, screen_height)

# Create a sprite group for ants
ants = pygame.sprite.Group()

# Place 5 ants randomly on the map
for _ in range(5):
    x = random.randint(0, 1600)  # Random x position within the world size
    y = random.randint(0, 1200)  # Random y position within the world size
    ant = Ant(x, y)
    ants.add(ant)

# Game loop
while running:
    screen.fill((0, 0, 0))  # Clear the screen

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button pressed
                camera.start_drag(event.pos)  # Start dragging

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button released
                camera.stop_drag()  # Stop dragging

    # If the mouse is dragging, update the camera's position
    if camera.dragging:
        mouse_pos = pygame.mouse.get_pos()
        camera.drag(mouse_pos)

    # Apply the camera movement to the distant background (slower movement for parallax effect)
    distant_offset_x = camera.camera.x * 0.3  # Slow down the movement for distant background (parallax effect)
    distant_offset_y = camera.camera.y * 0.3  # Slow down the movement for distant background (parallax effect)
    
    # Apply the camera movement to the main background (faster movement)
    background_offset_x = camera.camera.x * 0.6  # Faster movement for the main background (closer)
    background_offset_y = camera.camera.y * 0.6  # Faster movement for the main background (closer)
    
    # Draw the distant background (parallax effect, moves slower)
    distant_background_rect = pygame.Rect(distant_offset_x, distant_offset_y, *distant_background.get_size())
    screen.blit(distant_background, distant_background_rect)

    # Draw the main background (closer, moves faster)
    background_rect = pygame.Rect(background_offset_x, background_offset_y, *background.get_size())
    screen.blit(background, background_rect)

    # Draw the ants (apply camera offset)
    for ant in ants:
        screen.blit(ant.image, camera.apply(ant))

    # Update the display
    pygame.display.flip()

    # Set the FPS
    clock.tick(60)

pygame.quit()
