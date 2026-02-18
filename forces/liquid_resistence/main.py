
"""
Main simulation script for gravity and fluid resistance demonstration.

This script creates a pygame window with multiple movers that fall under
gravity and experience drag force when they enter a liquid region at the
bottom half of the screen. Click to reset the simulation.
"""

import random
from typing import List

import pygame
from pygame import Surface, Vector2
from liquid import Liquid
from mover import Mover

# Forces (Gravity and Fluid Resistence) with Vectors

# Demonstration of multiple force acting on bodies (Mover class)
# Bodies experience gravity continuously
# Bodies experience fluid resistance when in "water"

# Five moving bodies
movers: List[Mover] = []

# Liquid
liquid: Liquid = None


def setup() -> Surface:
    """
    Initialize the pygame display and create the simulation objects.
    
    Sets up a 640x360 window, creates multiple movers with random masses,
    and creates a liquid region in the bottom half of the screen.
    
    Returns:
        Surface: The pygame display surface
    """
    global liquid
    screen: Surface = pygame.display.set_mode((640, 360))
    reset(screen)
    # Create liquid object
    width: int = screen.get_width()
    height: int = screen.get_height()
    liquid = Liquid(screen, 0, height / 2, width, height / 2, 0.1)
    return screen


def draw(screen: Surface) -> None:
    """
    Handle the drawing and physics updates for each frame.
    
    This function:
    1. Clears the screen with white background
    2. Draws the liquid region
    3. For each mover:
       - Applies drag force if in liquid
       - Applies gravity (scaled by mass)
       - Updates physics
       - Renders the mover
       - Checks boundary collisions
    
    Args:
        screen: The pygame Surface to draw on
    """
    global liquid, movers
    screen.fill((255, 255, 255))

    # Draw liquid
    liquid.show()

    for i in range(len(movers)):
        # Is the Mover in the liquid?
        if liquid.contains(movers[i]):
            # Calculate drag force
            dragForce: Vector2 = liquid.calculateDrag(movers[i])
            # Apply drag force to Mover
            movers[i].applyForce(dragForce)

        # Gravity is scaled by mass here!
        gravity: Vector2 = pygame.Vector2(0, 0.1 * movers[i].mass)
        # Apply gravity
        movers[i].applyForce(gravity)

        # Update and display
        movers[i].update()
        movers[i].show()
        movers[i].checkEdges()


def reset(screen: Surface) -> None:
    """
    Reset the simulation by creating new movers.
    
    Creates 9 movers with random masses between 0.5 and 3.0,
    positioned horizontally across the top of the screen.
    
    Args:
        screen: The pygame Surface (used to position movers)
    """
    global movers
    movers = []
    for i in range(9):
        movers.append(Mover(screen, 40 + i * 70, 0, random.random() * 2.5 + 0.5))


if __name__ == "__main__":
    # Initialize pygame system
    pygame.init()
    
    # Set up the display and simulation objects
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
            # Reset simulation on mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                reset(screen)

        # Update and draw the frame
        draw(screen)

        # Update the display
        pygame.display.flip()
        
        # Maintain 60 frames per second
        clock.tick(60)