import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Ball:
    """
    Represents a bouncing ball with position, velocity, gravity, and damping properties.
    Attributes:
        x_pos (float): The x-coordinate of the ball's center.
        y_pos (float): The y-coordinate of the ball's center.
        x_vel (float): The velocity of the ball along the x-axis.
        y_vel (float): The velocity of the ball along the y-axis.
        gravity (float): The acceleration due to gravity applied to the ball.
        damping (float): The damping factor applied to the ball's velocity after bouncing.
        radius (float): The radius of the ball.
        color (str): The color of the ball.
    Methods:
        update():
            Updates the ball's position and velocity, applying gravity.
        check_boundaries(x_min, x_max, y_min, y_max):
            Checks and handles collisions with the boundaries defined by the given limits.
            Bounces the ball off the walls, floor, and ceiling, applying damping when hitting the floor.
    """

    def __init__(
        self,
        x_pos: float = 5,
        y_pos: float = 4,
        radius: float = 0.2,
        color: str = "red",
    ):
        # Initialize ball properties in this constructor
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = 0.07
        self.y_vel = 0.05
        self.gravity = 0.002
        self.damping = 0.9
        self.radius = radius
        self.color = color

    def update(self):
        """
        Updates the ball's position and velocity.

        Increments the x and y positions by their respective velocities,
        and applies gravity to the y velocity to simulate downward acceleration.
        """

        self.x_pos += self.x_vel
        self.y_pos += self.y_vel
        self.y_vel -= self.gravity  # Apply gravity

    def check_boundaries(
        self, x_min: float, x_max: float, y_min: float, y_max: float
    ) -> None:
        """
        Checks and handles collisions of the ball with the boundaries of the simulation area.

        If the ball collides with the left or right walls, its horizontal velocity is reversed.
        If the ball collides with the floor, its vertical velocity is reversed and damped, and its position is corrected to prevent passing through the floor.
        If the ball collides with the ceiling, its vertical velocity is reversed.

        Args:
            x_min (float): Minimum x-coordinate (left boundary).
            x_max (float): Maximum x-coordinate (right boundary).
            y_min (float): Minimum y-coordinate (bottom boundary).
            y_max (float): Maximum y-coordinate (top boundary).

        Returns:
            None
        """
        # Bounce off walls
        if self.x_pos < x_min + self.radius:  # Left wall
            self.x_vel = abs(self.x_vel)
        elif self.x_pos > x_max - self.radius:  # Right wall
            self.x_vel = -abs(self.x_vel)

        if self.y_pos < y_min + self.radius:  # Floor
            self.y_vel = abs(self.y_vel) * self.damping
            self.y_pos = y_min + self.radius  # Prevent going through floor
        elif self.y_pos > y_max - self.radius:  # Ceiling
            self.y_vel = -abs(self.y_vel)


class BallAnimation:
    """
    A class to animate a bouncing ball using Matplotlib with an object-oriented approach.

    This class sets up a Matplotlib figure and axis, creates a Ball object, and animates its movement
    within specified boundaries. The animation updates the ball's position and redraws it at each frame.

    Attributes:
        fig (matplotlib.figure.Figure): The Matplotlib figure object.
        ax (matplotlib.axes.Axes): The Matplotlib axes object.
        ball (Ball): The Ball object representing the bouncing ball.
        circle (matplotlib.patches.Circle): The graphical representation of the ball.

    Methods:
        init_animation():
            Initializes the animation by setting the ball's initial position.

        update_animation(frame):
            Updates the ball's physics and position for each animation frame.

        run():
            Starts the animation and displays the plot.

    #TODO: make the attributes able to be set in the constructor
    """

    def __init__(self):
        # Set up figure
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 8)
        self.ax.set_title("Bouncing Ball - Matplotlib (OOP)")

        # Create ball
        self.ball = Ball()
        self.circle = plt.Circle(
            (self.ball.x_pos, self.ball.y_pos), self.ball.radius, fc=self.ball.color
        )
        self.ax.add_patch(self.circle)

    def init_animation(self):
        """
        Initializes the animation by setting the circle's center to the current position of the ball.
        Returns:
            tuple: A tuple containing the circle artist to be used in the animation.
        """

        self.circle.center = (self.ball.x_pos, self.ball.y_pos)
        return (self.circle,)

    def update_animation(self, frame: int) -> tuple:
        """
        Updates the animation for each frame by advancing the ball's physics and checking boundary collisions.

        Args:
            frame (int): The current frame number of the animation.

        Returns:
            tuple: A tuple containing the updated matplotlib circle artist.
        """
        # Update ball physics
        self.ball.update()
        self.ball.check_boundaries(0, 10, 0, 8)

        # Update circle position
        self.circle.center = (self.ball.x_pos, self.ball.y_pos)
        return (self.circle,)

    def run(self):
        """
        Starts the matplotlib animation for the bouncing ball and displays the plot window.

        This method initializes a FuncAnimation object with the provided figure, update and
        initialization functions, number of frames, and interval between frames. The animation
        is displayed using plt.show(), which blocks execution until the plot window is closed.
        """
        self.animation = FuncAnimation(
            self.fig,
            self.update_animation,
            init_func=self.init_animation,
            frames=300,
            interval=30,
            blit=True,
        )
        plt.show()


# Run the animation
if __name__ == "__main__":
    animation = BallAnimation()
    animation.run()
