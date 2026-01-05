from vpython import *
from typing import Tuple, Any


class Ball:
    """
    A class representing a bouncing ball in a 3D simulation.

    This class encapsulates the properties and behaviors of a ball,
    including its position, velocity, radius, and collision physics.
    """

    def __init__(
        self, position: vector, radius: float, color: Any, velocity: vector
    ) -> None:
        """
        Initialize a new Ball object.

        Args:
            position: The initial position vector of the ball
            radius: The radius of the ball
            color: The color of the ball
            velocity: The initial velocity vector of the ball
        """
        self.position = position
        self.radius = radius
        self.velocity = velocity
        self.damping = 0.9
        self.sphere = sphere(pos=position, radius=radius, color=color)

    def update(self, dt: float, gravity: vector) -> None:
        """
        Update the ball's position and velocity based on physics.

        Args:
            dt: The time step for the physics simulation
            gravity: The gravity vector affecting the ball
        """
        # Update velocity and position
        self.velocity += gravity * dt
        self.sphere.pos += self.velocity * dt

    def check_boundaries(self, floor: box, walls: vector) -> None:
        """
        Check and respond to collisions with boundaries.

        Handles collisions with the floor and walls, applying appropriate
        bounce physics and ensuring the ball stays within the simulation area.

        Args:
            floor: The floor box object
            walls: The vector representing wall dimensions
        """
        # Check floor collision
        if self.sphere.pos.y - self.radius < floor.pos.y + floor.size.y / 2:
            self.velocity.y = abs(self.velocity.y) * self.damping
            self.sphere.pos.y = floor.pos.y + floor.size.y / 2 + self.radius

        # Check wall collisions
        if abs(self.sphere.pos.x) > walls.x - self.radius:
            self.velocity.x *= -1
            # Ensure ball stays within boundaries
            self.sphere.pos.x = sign(self.sphere.pos.x) * (walls.x - self.radius)

        if abs(self.sphere.pos.z) > walls.z - self.radius:
            self.velocity.z *= -1
            # Ensure ball stays within boundaries
            self.sphere.pos.z = sign(self.sphere.pos.z) * (walls.z - self.radius)


class BounceSimulation:
    """
    A class representing the entire bouncing ball simulation.

    Manages the simulation environment, physics parameters, and simulation loop.
    """

    def __init__(self) -> None:
        """
        Initialize the simulation environment and parameters.

        Sets up the scene, creates the environment, instantiates the ball,
        and defines physics parameters.
        """
        # Set up scene
        self.scene = canvas(
            width=800, height=600, title="Bouncing Ball - VPython (OOP)"
        )
        self.scene.range = 6
        self.scene.background = color.white

        # Define room dimensions
        self.room_width = 6
        self.room_length = 4
        self.room_height = 5

        # Create environment
        self.create_environment()

        # Create ball
        self.ball = Ball(
            position=vector(0, 3, 0),
            radius=0.5,
            color=color.red,
            velocity=vector(1, 0, 0.5),
        )

        # Physics parameters
        self.gravity = vector(0, -9.8, 0)
        self.dt = 0.01

    def create_environment(self) -> None:
        """
        Create the simulation environment.

        Sets up the floor and defines the wall boundaries for collision detection.
        """
        # Create floor
        self.floor = box(
            pos=vector(0, -self.room_height / 2, 0),
            size=vector(self.room_width, 0.1, self.room_length),
            color=color.gray(0.8),
        )

        # Room dimensions for collision detection
        self.walls = vector(
            self.room_width / 2, self.room_height / 2, self.room_length / 2
        )

    def run(self) -> None:
        """
        Run the main simulation loop.

        Updates the ball physics and handles collisions continuously.
        """
        # Main simulation loop
        while True:
            rate(100)  # Limit to 100 frames per second

            # Update ball physics
            self.ball.update(self.dt, self.gravity)
            self.ball.check_boundaries(self.floor, self.walls)


# Run the simulation
if __name__ == "__main__":
    simulation = BounceSimulation()
    simulation.run()
