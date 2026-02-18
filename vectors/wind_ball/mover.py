import pygame
from pygame import Vector2, Surface

class Mover:
    """
    A class representing a moving object with physics properties.
    
    This class simulates an object that can be affected by forces,
    following Newton's laws of motion. It tracks position, velocity,
    and acceleration, and handles boundary collision detection.
    
    Attributes:
        screen (pygame.Surface): The display surface to draw on
        mass (float): The mass of the mover (affects force calculations)
        position (pygame.Vector2): Current position of the mover
        velocity (pygame.Vector2): Current velocity of the mover
        acceleration (pygame.Vector2): Current acceleration of the mover
    """
    
    def __init__(self, screen: Surface) -> None:
        """
        Initialize a Mover object.
        
        Args:
            screen: The pygame Surface to draw the mover on
        """
        self.screen: Surface = screen
        self.mass: float = 1.0
        # Start at the center horizontally, near the top vertically
        self.position: Vector2 = Vector2(screen.get_width() / 2, 30)
        # Initialize with zero velocity (stationary)
        self.velocity: Vector2 = Vector2()
        # Initialize with zero acceleration
        self.acceleration: Vector2 = Vector2()

    def applyForce(self, force: Vector2) -> None:
        """
        Apply a force to the mover.
        
        Using Newton's second law: F = ma, therefore a = F/m
        The force is divided by mass to calculate acceleration.
        
        Args:
            force: A Vector2 representing the force to apply
        """
        # Calculate acceleration from force (F = ma, so a = F/m)
        f: Vector2 = force / self.mass
        # Add this acceleration to the current acceleration
        self.acceleration += f

    def update(self) -> None:
        """
        Update the mover's position based on velocity and acceleration.
        
        This implements the motion algorithm:
        1. Velocity changes by acceleration
        2. Position changes by velocity
        3. Acceleration is reset to zero (forces must be reapplied each frame)
        """
        # Update velocity by adding acceleration
        self.velocity += self.acceleration
        # Update position by adding velocity
        self.position += self.velocity
        # Reset acceleration to zero after applying (forces need to be reapplied)
        self.acceleration *= 0

    def show(self) -> None:
        """
        Draw the mover on the screen.
        
        Renders the mover as a filled circle with a black outline.
        """
        # Draw the filled circle body
        pygame.draw.circle(self.screen, "gray50", self.position, 24)
        # Draw the black outline (stroke)
        pygame.draw.circle(self.screen, "black", self.position, 24, 2)

    def checkEdges(self) -> None:
        """
        Check if the mover has hit the screen edges and bounce if so.
        
        When the mover hits an edge, its position is constrained to the boundary
        and its velocity in that direction is reversed (bouncing effect).
        """
        # Check right edge
        if self.position.x > self.screen.get_width():
            self.position.x = self.screen.get_width()
            self.velocity.x *= -1  # Reverse horizontal direction
        # Check left edge
        elif self.position.x < 0:
            self.velocity.x *= -1  # Reverse horizontal direction
            self.position.x = 0

        # Check bottom edge
        if self.position.y > self.screen.get_height():
            self.velocity.y *= -1  # Reverse vertical direction
            self.position.y = self.screen.get_height()