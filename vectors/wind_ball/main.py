import pygame
from forces.wind_ball.mover import Mover

"""
Main simulation script for physics-based mover demonstration.

This script creates a pygame window with a mover object that responds
to gravity and optional wind forces controlled by mouse input.
"""

import pygame
from pygame import Surface, Vector2
from forces.wind_ball.mover import Mover

# Global variable to store the mover instance
mover: Mover = None


def setup() -> Surface:
    """
    Initialize the pygame display and create the mover object.
    
    Sets up a 640x360 window and creates a Mover instance.
    Prints instructions for user interaction.
    
    Returns:
        Surface: The pygame display surface
    """
    global mover
    screen: Surface = pygame.display.set_mode((640, 360))
    mover = Mover(screen)
    print("Click mouse to apply wind force")
    return screen


def draw(screen: Surface) -> None:
    """
    Handle the drawing and physics updates for each frame.
    
    This function:
    1. Clears the screen with white background
    2. Applies constant gravity force
    3. Applies wind force when mouse is pressed
    4. Updates mover physics
    5. Checks for boundary collisions
    6. Renders the mover
    
    Args:
        screen: The pygame Surface to draw on
    """
    global mover
    # Clear screen with white background
    screen.fill((255, 255, 255))
    
    # Apply constant downward gravity force
    gravity: Vector2 = pygame.Vector2(0, 0.1)
    mover.applyForce(gravity)
    
    # Apply wind force when left mouse button is pressed
    if pygame.mouse.get_pressed()[0]:
        wind: Vector2 = pygame.Vector2(0.1, 0)
        mover.applyForce(wind)
    
    # Update physics calculations
    mover.update()
    # Check and handle boundary collisions
    mover.checkEdges()
    # Render the mover on screen
    mover.show()


if __name__ == "__main__":
    # Initialize pygame system
    pygame.init()
    
    # Set up the display and mover
    screen: Surface = setup()
    
    # Create clock object to control frame rate
    clock: pygame.time.Clock = pygame.time.Clock()
    
    # Main game loop flag
    running: bool = True
    
    # Main game loop
    while running:
        # Handle events
        for event in pygame.event.get():
            # Check for window close event
            if event.type == pygame.QUIT:
                running = False
        
        # Update and draw the frame
        draw(screen)
        
        # Update the display
        pygame.display.flip()
        
        # Maintain 60 frames per second
        clock.tick(60)