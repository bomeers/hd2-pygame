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

# Load the background images (Star-Map.bmp as the main background and a distant layer)
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
        self.zoom_level = 1  # Default zoom level (1 = zoomed-in)

    def apply(self, entity):
        """Moves the entity based on camera position."""
        # Scale entity position based on zoom level
        return entity.rect.move(self.camera.topleft).inflate(entity.rect.width * (self.zoom_level - 1), entity.rect.height * (self.zoom_level - 1))

    def start_drag(self, pos):
        """Initiates dragging when mouse is pressed."""
        if self.zoom_level == 1:  # Only allow dragging when zoomed in
            self.dragging = True
            self.drag_start_pos = pos

    def stop_drag(self):
        """Stops dragging when mouse is released."""
        self.dragging = False

    def drag(self, pos):
        """Update camera position based on drag movement."""
        if self.zoom_level == 1 and self.dragging:  # Only allow dragging when zoomed in
            dx = pos[0] - self.drag_start_pos[0]
            dy = pos[1] - self.drag_start_pos[1]
            self.camera.x += dx
            self.camera.y += dy
            self.drag_start_pos = pos  # Update the drag start position

    def toggle_zoom(self):
        """Toggle between two zoom levels: zoomed-in and zoomed-out."""
        if self.zoom_level == 1:
            self.zoom_level = 0.5  # Zoomed out
        else:
            self.zoom_level = 1  # Zoomed in

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

# Variable to track double-click timing
last_click_time = 0
double_click_threshold = 300  # Maximum time in milliseconds between clicks for a double-click

# Game loop
while running:
    screen.fill((0, 0, 0))  # Clear the screen

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button pressed
                # Get the current time
                current_time = pygame.time.get_ticks()
                if current_time - last_click_time <= double_click_threshold:
                    # Double-click detected, toggle zoom
                    camera.toggle_zoom()
                last_click_time = current_time  # Update last click time

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
    
    # Scale the backgrounds based on zoom level
    scaled_background = pygame.transform.scale(background, (int(background.get_width() * camera.zoom_level), int(background.get_height() * camera.zoom_level)))
    scaled_distant_background = pygame.transform.scale(distant_background, (int(distant_background.get_width() * camera.zoom_level), int(distant_background.get_height() * camera.zoom_level)))
    
    # Draw the distant background (parallax effect, moves slower)
    distant_background_rect = pygame.Rect(distant_offset_x, distant_offset_y, *scaled_distant_background.get_size())
    screen.blit(scaled_distant_background, distant_background_rect)

    # Draw the main background (closer, moves faster)
    background_rect = pygame.Rect(background_offset_x, background_offset_y, *scaled_background.get_size())
    screen.blit(scaled_background, background_rect)

    # Draw the ants (apply camera offset and scaling)
    for ant in ants:
        screen.blit(ant.image, camera.apply(ant))

    # Update the display
    pygame.display.flip()

    # Set the FPS
    clock.tick(60)

pygame.quit()
