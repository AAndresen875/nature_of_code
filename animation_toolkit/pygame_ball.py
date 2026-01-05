import pygame
import sys
import math
from typing import Tuple, Optional, List, Union


class Ball:
    """
    A simple ball class for simulating a bouncing ball with gravity and boundary collision.

    Attributes:
        x (float): The x-coordinate of the ball's center.
        y (float): The y-coordinate of the ball's center.
        radius (int): The radius of the ball.
        color (tuple): The RGB color of the ball.
        velocity_x (float): The velocity of the ball along the x-axis.
        velocity_y (float): The velocity of the ball along the y-axis.
        gravity (float): The acceleration due to gravity applied to the ball.
    """

    def __init__(self, x: float, y: float, radius: int, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity_x = 3
        self.velocity_y = 2
        self.gravity = 0.1

    def update(self) -> None:
        """
        Update the ball's position based on its current velocity.

        This method should be called every frame to move the ball.
        """
        self.x += self.velocity_x
        self.y += self.velocity_y
        # Apply gravity
        self.velocity_y += self.gravity

    def check_boundaries(self, width: int, height: int) -> None:
        """
        Checks and handles collisions of the object with the boundaries of the screen.

        If the object collides with the left or right boundaries, its horizontal velocity is reversed.
        If the object collides with the top or bottom boundaries, its vertical velocity is reversed and dampened.
        The object's position is also clamped to ensure it remains within the visible area.

        Args:
            width (int): The width of the screen or boundary.
            height (int): The height of the screen or boundary.

        Returns:
            None

        Logic explanation:
        - If the object's position plus/minus its radius exceeds the screen boundaries (left/right or top/bottom),
        - its velocity is reversed (bounces off the wall).
        - For vertical boundaries, velocity is also dampened to simulate energy loss.
        - The object's position is clamped so it never goes outside the visible area.
        """
        # Bounce off walls
        # Check if the ball has collided with any of the screen boundaries and handle the bounce logic
        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            self.velocity_x *= -1
            # Ensure ball stays within boundaries
            self.x = max(self.radius, min(width - self.radius, self.x))

        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            self.velocity_y *= -0.9  # Damping effect
            # Ensure ball stays within boundaries
            self.y = max(self.radius, min(height - self.radius, self.y))

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the ball on the given Pygame screen surface.

        Args:
            screen (pygame.Surface): The surface to draw the ball on.

        Logic explanation:
        - Uses pygame.draw.circle to render the ball at its current (x, y) position.
        - The position is cast to integers as required by Pygame.
        - The ball's color and radius are used for rendering.
        - This method should be called every frame after updating the ball's position.

        Returns:
            None
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


class Game:
    """
    Main game class that handles the game loop, rendering, and physics updates.

    Attributes:
        width (int): Width of the game window.
        height (int): Height of the game window.
        screen (pygame.Surface): Pygame surface for rendering.
        WHITE (Tuple[int, int, int]): RGB color value for white.
        RED (Tuple[int, int, int]): RGB color value for red.
        ball (Ball): Ball object that will be animated.
        clock (pygame.time.Clock): Clock for controlling frame rate.
    """

    def __init__(self, width: int = 800, height: int = 600) -> None:
        """
        Initializes the Pygame animation toolkit window and sets up the environment.

        Args:
            width (int, optional): The width of the window. Defaults to 800.
            height (int, optional): The height of the window. Defaults to 600.

        Initializes:
            - Pygame library.
            - Display window with specified width and height.
            - Window caption.
            - Color constants (WHITE, RED).
            - Ball object positioned at the center of the window.
            - Pygame clock for managing frame rate.
        """
        # Initialize Pygame
        pygame.init()

        # Set up display
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bouncing Ball - Pygame (OOP)")

        # Colors
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)

        # Create ball
        self.ball = Ball(width // 2, height // 2, 20, self.RED)

        # Set up clock
        self.clock = pygame.time.Clock()

    def handle_events(self) -> bool:
        """
        Handles incoming Pygame events, specifically checking for the QUIT event.

        Iterates through the event queue and returns False if a QUIT event is detected,
        which is typically triggered when the user attempts to close the application window.
        This method is essential for managing the application's main loop and ensuring
        a graceful shutdown when the user requests to exit.

        Returns:
            bool: False if a QUIT event is detected, True otherwise.
        """
        # Process all events in the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update(self) -> None:
        """
        Updates the state of the ball and checks if it remains within the boundaries of the window.

        This method calls the `update` method of the ball to advance its position or state,
        and then checks if the ball is within the defined width and height boundaries,
        adjusting its position if necessary.
        """
        self.ball.update()
        self.ball.check_boundaries(self.width, self.height)

    def draw(self) -> None:
        """
        Clears the screen, draws the ball object, and updates the display.

        This method fills the screen with a white background, renders the ball
        onto the screen, and then refreshes the display to show the updated frame.
        """
        self.screen.fill(self.WHITE)
        self.ball.draw(self.screen)
        pygame.display.flip()

    def run(self) -> None:
        """
        Starts the main loop of the animation toolkit.

        Continuously processes events, updates the animation state, and redraws the screen
        at a fixed frame rate (60 FPS) until the application is closed. Cleans up resources
        and exits the program when the loop ends.
        """
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Cap at 60 FPS

        pygame.quit()
        sys.exit()


# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()


import pygame
import sys
import random
import math
from typing import Tuple, List, Union, Optional


class Vector2D:
    """
    A simple 2D vector class for representing and manipulating vectors in two-dimensional space.

    Attributes:
        x (float): The x-component of the vector.
        y (float): The y-component of the vector.

    Methods:
        add(other: Vector2D) -> Vector2D:
            Returns a new Vector2D that is the sum of this vector and another.
        multiply(scalar: float) -> Vector2D:
            Returns a new Vector2D that is this vector scaled by the given scalar.
        magnitude() -> float:
            Returns the magnitude (length) of the vector.
        normalize() -> Vector2D:
            Returns a new Vector2D that is the normalized (unit length) version of this vector.
    """

    def __init__(self, x: float = 0, y: float = 0) -> None:
        """
        Initialize an object with x and y coordinates.

        Args:
            x (float, optional): The x-coordinate. Defaults to 0.
            y (float, optional): The y-coordinate. Defaults to 0.
        """
        self.x = x
        self.y = y

    def add(self, other: "Vector2D") -> "Vector2D":
        """
        Adds the components of another Vector2D to this vector and returns a new Vector2D instance.

        Args:
            other (Vector2D): The vector to add.

        Returns:
            Vector2D: A new vector representing the sum of this vector and the other.
        """
        return Vector2D(self.x + other.x, self.y + other.y)

    def multiply(self, scalar: float) -> "Vector2D":
        """
        Multiplies the vector by a scalar value.

        Args:
            scalar (float): The value to multiply the vector by.

        Returns:
            Vector2D: A new vector that is the result of the multiplication.
        """
        return Vector2D(self.x * scalar, self.y * scalar)

    def magnitude(self) -> float:
        """
        Calculate and return the magnitude (length) of the vector.

        Returns:
            float: The Euclidean norm of the vector, computed as sqrt(x^2 + y^2).
        """
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self) -> "Vector2D":
        """
        Returns a normalized (unit length) vector in the same direction as this vector.

        Calculates the magnitude of the vector and divides each component by the magnitude.
        If the magnitude is zero, returns a zero vector.

        Returns:
            Vector2D: A new Vector2D instance with unit length in the same direction,
                      or a zero vector if the original vector has zero magnitude.
        """
        mag = self.magnitude()
        if mag > 0:
            return Vector2D(self.x / mag, self.y / mag)
        return Vector2D(0, 0)


class PhysicsObject:
    """
    Represents a physics object with position, velocity, acceleration, and mass.

    This class provides basic physics simulation capabilities, allowing forces to be applied
    and updating the object's state over time using simple Newtonian mechanics.

    Attributes:
        position (Vector2D): The current position of the object.
        velocity (Vector2D): The current velocity of the object.
        acceleration (Vector2D): The current acceleration of the object.
        mass (float): The mass of the object, affecting its response to applied forces.

    Methods:
        apply_force(force: Vector2D) -> None:
            Applies a force to the object, updating its acceleration according to F = ma.
        update(dt: float = 1.0) -> None:
            Updates the object's velocity and position based on its acceleration and the time step.
            Resets acceleration after each update.
    """

    def __init__(
        self, position: Vector2D, velocity: Vector2D, mass: float = 1.0
    ) -> None:
        """
        Initialize a new object with position, velocity, and mass.

        Args:
            position (Vector2D): The initial position of the object.
            velocity (Vector2D): The initial velocity of the object.
            mass (float, optional): The mass of the object. Defaults to 1.0.

        Attributes:
            position (Vector2D): Current position of the object.
            velocity (Vector2D): Current velocity of the object.
            acceleration (Vector2D): Current acceleration of the object, initialized to zero.
            mass (float): Mass of the object.
        """
        self.position = position
        self.velocity = velocity
        self.acceleration = Vector2D(0, 0)
        self.mass = mass

    def apply_force(self, force: Vector2D) -> None:
        """
        Applies a force to the object, updating its acceleration according to Newton's second law (F = ma).

        Args:
            force (Vector2D): The force vector to apply.

        Updates:
            self.acceleration: Increases by the force divided by the object's mass.
        """
        # F = ma → a = F/m
        f = force.multiply(1.0 / self.mass)
        self.acceleration = self.acceleration.add(f)

    def update(self, dt: float = 1.0) -> None:
        """
        Updates the object's position and velocity based on its current acceleration and the elapsed time.

        Args:
            dt (float, optional): The time step for the update. Defaults to 1.0.

        Side Effects:
            - Updates the velocity by adding the product of acceleration and dt.
            - Updates the position by adding the product of velocity and dt.
            - Resets acceleration to zero after the update.
        """
        # Update velocity
        self.velocity = self.velocity.add(self.acceleration.multiply(dt))

        # Update position
        self.position = self.position.add(self.velocity.multiply(dt))

        # Reset acceleration
        self.acceleration = Vector2D(0, 0)


class Ball(PhysicsObject):
    """
    Represents a bouncing ball in a 2D physics simulation.

    Inherits from PhysicsObject and adds radius, color, and boundary collision logic.

    Attributes:
        position (Vector2D): Center position of the ball.
        velocity (Vector2D): Current velocity of the ball.
        radius (int): Radius of the ball.
        color (tuple): RGB color of the ball.
        mass (float): Mass of the ball.
        damping (float): Energy loss factor on collision.
    """

    def __init__(
        self,
        x: float,
        y: float,
        radius: int,
        color: Tuple[int, int, int],
        mass: float = 1.0,
    ) -> None:
        """
        Initializes a Ball object with position, velocity, radius, color, and mass.

        Args:
            x (float): Initial x-coordinate of the ball's center.
            y (float): Initial y-coordinate of the ball's center.
            radius (int): Radius of the ball.
            color (tuple): RGB color of the ball.
            mass (float, optional): Mass of the ball. Defaults to 1.0.
        """
        super().__init__(
            Vector2D(x, y), Vector2D(random.uniform(-2, 2), random.uniform(-2, 2)), mass
        )
        self.radius: int = radius
        self.color: Tuple[int, int, int] = color
        self.damping: float = 0.9  # Energy loss on collision

    def check_boundaries(self, width: int, height: int) -> None:
        """
        Checks and handles collisions of the ball with the boundaries of the screen.

        Args:
            width (int): Width of the screen.
            height (int): Height of the screen.

        Logic:
            - If the ball collides with the left/right/top/bottom boundaries,
              its velocity is reversed and dampened.
            - The ball's position is clamped to remain within the visible area.
        """
        if self.position.x - self.radius < 0:
            self.position.x = self.radius
            self.velocity.x *= -self.damping
        elif self.position.x + self.radius > width:
            self.position.x = width - self.radius
            self.velocity.x *= -self.damping

        if self.position.y - self.radius < 0:
            self.position.y = self.radius
            self.velocity.y *= -self.damping
        elif self.position.y + self.radius > height:
            self.position.y = height - self.radius
            self.velocity.y *= -self.damping

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the ball on the given Pygame screen surface.

        Args:
            screen (pygame.Surface): The surface to draw the ball on.
        """
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.position.x), int(self.position.y)),
            self.radius,
        )


class Physics:
    """
    Static class providing physics-related utility functions for simulations.

    This class contains methods for handling physical interactions between objects,
    such as collision detection and resolution between balls.
    """

    @staticmethod
    def check_collision(ball1: Ball, ball2: Ball) -> None:
        """
        Checks and resolves collisions between two balls using physics principles.

        Args:
            ball1 (Ball): First ball to check for collision.
            ball2 (Ball): Second ball to check for collision.

        Logic:
            1. Calculate the vector between ball centers
            2. Check if balls are overlapping based on their radii
            3. If colliding, calculate the collision normal and relative velocity
            4. Resolve the collision by applying impulse forces to both balls
            5. Separate the balls to prevent sticking/penetration
        """
        # Vector between centers
        distance = Vector2D(
            ball2.position.x - ball1.position.x, ball2.position.y - ball1.position.y
        )

        # Magnitude of distance
        dist_magnitude = distance.magnitude()

        # Check if balls are colliding
        if dist_magnitude < ball1.radius + ball2.radius:
            # Normalize the distance vector
            normal = distance.normalize()

            # Relative velocity
            rel_velocity = Vector2D(
                ball2.velocity.x - ball1.velocity.x, ball2.velocity.y - ball1.velocity.y
            )

            # Velocity along collision normal
            vel_along_normal = rel_velocity.x * normal.x + rel_velocity.y * normal.y

            # Only resolve collision if objects are moving toward each other
            if vel_along_normal < 0:
                # Calculate impulse scalar
                restitution = 0.9  # Coefficient of restitution

                # Calculate impulse scalar
                j = -(1 + restitution) * vel_along_normal
                j /= 1 / ball1.mass + 1 / ball2.mass

                # Apply impulse
                impulse = normal.multiply(j)

                # Update velocities
                ball1.velocity.x -= impulse.x * (1 / ball1.mass)
                ball1.velocity.y -= impulse.y * (1 / ball1.mass)
                ball2.velocity.x += impulse.x * (1 / ball2.mass)
                ball2.velocity.y += impulse.y * (1 / ball2.mass)

                # Separate balls to prevent sticking
                overlap = (ball1.radius + ball2.radius - dist_magnitude) * 0.5
                ball1.position.x -= normal.x * overlap
                ball1.position.y -= normal.y * overlap
                ball2.position.x += normal.x * overlap
                ball2.position.y += normal.y * overlap


class BounceSimulation:
    """
    Main simulation class for multiple bouncing balls with physics.

    This class manages the entire simulation, including:
    - Creating and updating multiple balls
    - Handling user input (adding new balls with mouse clicks)
    - Detecting and resolving collisions between balls
    - Applying gravity and other forces
    - Rendering the scene

    Attributes:
        width (int): Width of the simulation window.
        height (int): Height of the simulation window.
        screen (pygame.Surface): Pygame surface for rendering.
        balls (List[Ball]): List of Ball objects in the simulation.
        gravity (Vector2D): Gravity force vector applied to all balls.
        clock (pygame.time.Clock): Clock for controlling frame rate.
    """

    def __init__(self, width: int = 800, height: int = 600, num_balls: int = 5) -> None:
        """
        Initialize the simulation with configurable parameters.

        Args:
            width (int, optional): Width of the simulation window. Defaults to 800.
            height (int, optional): Height of the simulation window. Defaults to 600.
            num_balls (int, optional): Initial number of balls. Defaults to 5.
        """
        # Initialize Pygame
        pygame.init()

        # Set up display
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Multiple Bouncing Balls - Advanced OOP")

        # Colors
        self.WHITE = (255, 255, 255)
        self.COLORS: List[Tuple[int, int, int]] = [
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (255, 165, 0),  # Orange
            (128, 0, 128),  # Purple
        ]

        # Create balls
        self.balls: List[Ball] = []
        for i in range(num_balls):
            radius = random.randint(20, 40)
            mass = radius / 10.0  # Mass proportional to size
            x = random.randint(radius, width - radius)
            y = random.randint(radius, height - radius)
            color = random.choice(self.COLORS)
            self.balls.append(Ball(x, y, radius, color, mass))

        # Gravity force
        self.gravity = Vector2D(0, 0.1)

        # Set up clock
        self.clock = pygame.time.Clock()

    def handle_events(self) -> bool:
        """
        Handles Pygame events and user input.

        Returns:
            bool: False if the user wants to quit, True otherwise.

        Features:
            - Quits when the user closes the window
            - Creates a new ball at the mouse position when clicked
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Add new ball on mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                radius = random.randint(20, 40)
                color = random.choice(self.COLORS)
                mass = radius / 10.0
                self.balls.append(Ball(x, y, radius, color, mass))

        return True

    def update(self) -> None:
        """
        Updates the physics simulation for all balls.

        This method:
        1. Applies gravity to all balls
        2. Updates the position of all balls
        3. Checks for collisions with boundaries
        4. Checks for collisions between all pairs of balls
        """
        # Apply gravity to all balls
        for ball in self.balls:
            ball.apply_force(self.gravity)
            ball.update()
            ball.check_boundaries(self.width, self.height)

        # Check for collisions between all pairs of balls
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                Physics.check_collision(self.balls[i], self.balls[j])

    def draw(self) -> None:
        """
        Renders all simulation objects to the screen.

        Clears the screen, draws all balls, and updates the display.
        """
        self.screen.fill(self.WHITE)
        for ball in self.balls:
            ball.draw(self.screen)
        pygame.display.flip()

    def run(self) -> None:
        """
        Runs the main simulation loop.

        Continuously handles events, updates physics, and renders at 60 FPS
        until the user chooses to quit.
        """
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Cap at 60 FPS

        pygame.quit()
        sys.exit()


# Run the simulation
if __name__ == "__main__":
    simulation = BounceSimulation()
    simulation.run()
