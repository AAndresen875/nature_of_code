import pygame
import random

class Particle():
    def __init__(self, x: int, y: int, color: tuple, 
                 radius: int, mass = 1, velocity = None, acceleration = None):
        
        self.color = color
        self.mass = mass
        self.lifespan = 255
        self.radius = radius
        self.rect = pygame.Rect(x - radius, y - radius, radius*2, radius*2)

        # this are all pygame Vectors
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity if velocity is not None else pygame.Vector2(0, 0)
        self.acceleration = acceleration if acceleration is not None else pygame.Vector2(0, 0)
        
    def apply_force(self, force: pygame.Vector2):
        """
        Applies a force on the Mover object (i.e. gravity), follows Newton's formula F = m x A

        Args:
            - force -> force to be applied
        """
        force_copy = force.copy()
        f = force_copy / self.mass  
        self.acceleration += f 

    def update_position(self):
        """
        Updates the position of the mover, used after a force is applied via apply_force().
        """
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0 
        self.rect = pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius*2, self.radius*2)


    def draw(self, screen):
        """
        Draw the object on the canvas.
        """
        alpha = max(0, min(255, self.lifespan))
        temp_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        faded_color = (*self.color, alpha) 
        pygame.draw.circle(temp_surface, faded_color, (self.radius, self.radius), self.radius)
        screen.blit(temp_surface, (self.rect.x, self.rect.y))
        self.lifespan -= 3

    def is_dead(self):
        """
        Checks whether the particle is still alive.
        It's used when we want to get rid of a particle.
        """
        return self.lifespan < 0
    
    def run(self, screen):
        self.update_position()
        self.draw(screen)