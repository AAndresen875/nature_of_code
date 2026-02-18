"""
Mover class for simulating objects with physics properties.

This module defines a Mover object that responds to forces and follows
Newton's laws of motion with gravity and fluid resistance.
"""

import pygame
from pygame import Surface, Vector2


class Mover:
    """
    A class representing a moving object with physics properties.
    
    This class simulates an object that can be affected by forces,
    following Newton's laws of motion. It tracks position, velocity,
    acceleration, and mass. The mover bounces off the bottom edge with dampening.
    
    Attributes:
        screen (Surface): The display surface to draw on
        mass (float): The mass of the mover (affects force calculations and size)
        radius (float): The visual radius of the mover (scaled by mass)
        position (Vector2): Current position of the mover
        velocity (Vector2): Current velocity of the mover
        acceleration (Vector2): Current acceleration of the mover
    """
    
    def __init__(self, screen: Surface, x: float, y: float, m: float) -> None:
        """
        Initialize a Mover object.
        
        Args:
            screen: The pygame Surface to draw the mover on
            x: Initial x-coordinate
            y: Initial y-coordinate
            m: Mass of the mover
        """
        self.screen: Surface = screen
        self.mass: float = m
        self.radius: float = m * 8
        self.position: Vector2 = pygame.Vector2(x, y)
        self.velocity: Vector2 = pygame.Vector2()
        self.acceleration: Vector2 = pygame.Vector2()

    def applyForce(self, force: Vector2) -> None:
        """
        Apply a force to the mover.
        
        Using Newton's second law: F = M * A, therefore A = F / M
        The force is divided by mass to calculate acceleration.
        
        Args:
            force: A Vector2 representing the force to apply
        """
        f: Vector2 = force / self.mass
        self.acceleration += f

    def update(self) -> None:
        """
        Update the mover's position based on velocity and acceleration.
        
        This implements the motion algorithm:
        1. Velocity changes by acceleration
        2. Position changes by velocity
        3. Acceleration is reset to zero (forces must be reapplied each frame)
        """
        # Velocity changes according to acceleration
        self.velocity += self.acceleration
        # position changes by velocity
        self.position += self.velocity
        # We must clear acceleration each frame
        self.acceleration *= 0

    def show(self) -> None:
        """
        Draw the mover on the screen.
        
        Renders the mover as a filled circle with anti-aliasing and a black outline.
        The size is determined by the radius (which is based on mass).
        """
        pygame.draw.circle(self.screen, "gray50", self.position, self.radius)
        pygame.draw.circle(self.screen, "black", self.position, self.radius, 2)

    def checkEdges(self) -> None:
        """
        Check if the mover has hit the bottom edge and bounce if so.
        
        When the mover hits the bottom, its vertical velocity is reversed
        and dampened (multiplied by -0.9) to simulate energy loss.
        The position is also constrained to prevent sinking below the edge.
        """
        if self.position.y > self.screen.get_height() - self.radius:
            self.velocity.y *= -0.9  # A little dampening when hitting the bottom
            self.position.y = self.screen.get_height() - self.radius
