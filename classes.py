import pygame

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)  # Initial camera position
        self.world_size = (width * 2, height * 2)  # World size (example: double the size of the window)
        self.window_size = (width, height)  # Window size
        self.dragging = False  # To track if the user is dragging the camera
        self.drag_start_pos = None  # Start position of the drag
        self.camera.center = (0,0)
        # self.zoom_default = 4
        # self.zoom_level = 0.5  # Default zoom level (1 = zoomed-in)

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
        if self.dragging:  # Only allow dragging when zoomed in
            dx = pos[0] - self.drag_start_pos[0]
            dy = pos[1] - self.drag_start_pos[1]
            self.camera.x += dx
            self.camera.y += dy
            self.drag_start_pos = pos  # Update the drag start position

            self.camera.x = max(-480, min(self.camera.x, 0))
            self.camera.y = max(-480, min(self.camera.y, 0))
        
    # TODO: implement this later when adding zoom
    # def smoothZoom(camera, target_zoom, speed=0.1):
    #     """Smoothly interpolate the camera zoom towards the target zoom level."""
    #     camera.zoom = camera.zoom + (target_zoom - camera.zoom) * speed

class Planet(pygame.sprite.Sprite):
    def __init__(self, index, name, sector, biome, owner, health, regenPerSecond, players, x, y, image):
        super().__init__()
        self.index = index
        self.name = name
        self.sector = sector
        self.biome = biome
        self.owner = owner
        self.health = health
        self.regenPerSecond = regenPerSecond
        self.players = players
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self, surface, camera, font):
        # Apply camera transformation to the planet's position
        screen_pos = camera.apply(self)
        surface.blit(self.image, screen_pos)
        
        # Render and position the planet name below the planet image
        text_surface = font.render(self.name, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen_pos.centerx, screen_pos.bottom + 10))
        surface.blit(text_surface, text_rect.topleft)