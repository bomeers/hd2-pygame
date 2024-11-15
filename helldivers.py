import pygame
import math  # Import math module for trigonometric functions

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 480, 480  # Window size
ZOOM_FACTOR = 4  # Zoom factor for each double click (for both zoom in and zoom out)
DOUBLE_CLICK_TIME = 500  # Maximum time (in milliseconds) between clicks for a double-click
RADIUS = 240  # Radius of the circular boundary (half of 480px diameter)

# Set up the Pygame screen without the title bar (no frame)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Double Click to Zoom and Drag Image")

# Resize the image while maintaining the aspect ratio
def resize_image(image, target_width, target_height):
    img_width, img_height = image.get_size()
    aspect_ratio = img_width / img_height

    if aspect_ratio > 1:  # Wide image
        new_width = target_width
        new_height = target_width / aspect_ratio
    else:  # Tall image
        new_height = target_height
        new_width = target_height * aspect_ratio

    # Cast the new dimensions to integers before passing to scale
    return pygame.transform.scale(image, (int(new_width), int(new_height)))

# Load the image from a local file
image_path = "Star-Map.jpg"  # Assuming the image is in the same folder as the script
image = pygame.image.load(image_path)

# Resize the image to fit the screen (initially, at its original aspect ratio)
image = resize_image(image, WIDTH, HEIGHT)
image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Variables for dragging, zooming, and zoom state
dragging = False
offset_x = 0
offset_y = 0
zoom_level = 1.0  # Current zoom level
zoomed_in = False  # Keep track of whether the image is zoomed in or not
last_click_time = 0  # Time of the last mouse click
double_click = False  # Flag to indicate if it's a double-click

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Check for Escape key to exit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False  # Exit the game loop when Escape is pressed

        # Mouse button events for dragging and zooming
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button for zoom in/out and drag
                current_time = pygame.time.get_ticks()
                
                # Check for double-click (within DOUBLE_CLICK_TIME milliseconds)
                if current_time - last_click_time <= DOUBLE_CLICK_TIME:
                    double_click = True
                else:
                    double_click = False

                last_click_time = current_time  # Update the last click time
                
                # If it's a double-click, zoom in or out
                if double_click:
                    if zoomed_in:
                        # Zoom out
                        zoom_level /= ZOOM_FACTOR
                    else:
                        # Zoom in
                        zoom_level *= ZOOM_FACTOR
                    
                    # Update the zoom state
                    zoomed_in = not zoomed_in

                    # Resize the image based on the new zoom level
                    image = resize_image(pygame.image.load(image_path), WIDTH * zoom_level, HEIGHT * zoom_level)
                    image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

                # Start dragging
                if not double_click:  # Don't start dragging if it's a double-click
                    if image_rect.collidepoint(event.pos):
                        dragging = True
                        offset_x = image_rect.x - event.pos[0]
                        offset_y = image_rect.y - event.pos[1]

        elif event.ty
