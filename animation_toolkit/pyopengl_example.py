"""pyopengl_example.py

Simple 3D random walker rendered with PyOpenGL and GLFW.
This module demonstrates a basic OpenGL setup, a rotating camera,
and a RandomWalker that leaves a fading trail behind it.
"""

from OpenGL.GL import (
    glClearColor, glEnable, glBlendFunc, glLineWidth, glColorMaterial,
    glLightfv, glClear, glLoadIdentity, glRotatef, glDisable, glBegin,
    glColor3f, glVertex3f, glEnd, glPushMatrix, glTranslatef, glPopMatrix,
    GL_DEPTH_TEST, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA,
    GL_LINE_SMOOTH, GL_LIGHTING, GL_LIGHT0, GL_COLOR_MATERIAL,
    GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, GL_POSITION, GL_AMBIENT,
    GL_DIFFUSE, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_LINE_STRIP,
    GL_LINES, glMatrixMode, GL_PROJECTION, GL_MODELVIEW, glViewport
)

from OpenGL.GLU import gluPerspective, gluLookAt

import glfw
import sys
import random
from typing import Any, List, Optional, Tuple

class RandomWalker3D:
    """A simple 3D random walker with a limited trail history.

    Attributes:
        x (float): Current x position.
        y (float): Current y position.
        z (float): Current z position.
        history (List[Tuple[float, float, float]]): List of previous positions.
        max_history (int): Maximum number of stored positions in history.
    """

    def __init__(self) -> None:
        """Initialize the walker's position and history."""
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0
        self.history: List[Tuple[float, float, float]] = [(0.0, 0.0, 0.0)]
        self.max_history: int = 500

    def step(self) -> None:
        """Advance the walker by a fixed step in a random axis.

        The walker randomly chooses one of six directions (+/- x, +/- y, +/- z)
        and appends the new position to the history buffer. If the history
        exceeds ``max_history``, the oldest sample is discarded.
        """
        step_size: float = 0.5
        direction: int = random.randint(0, 5)

        # Move in one of the 6 cardinal directions
        if direction == 0:
            self.x += step_size
        elif direction == 1:
            self.x -= step_size
        elif direction == 2:
            self.y += step_size
        elif direction == 3:
            self.y -= step_size
        elif direction == 4:
            self.z += step_size
        else:
            self.z -= step_size

        # Record new position and enforce history length
        self.history.append((self.x, self.y, self.z))
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def display(self) -> None:
        """Render the walker's trail and a small local axis marker.

        The trail is drawn as a line strip with a fading color gradient to
        indicate older positions. A small red/green/blue cross marks the
        current walker position.
        """
        # Draw trail if we have more than one point
        if len(self.history) > 1:
            glBegin(GL_LINE_STRIP)
            for i, (x, y, z) in enumerate(self.history):
                fade: float = i / len(self.history)  # older points are darker
                glColor3f(0.0, fade * 0.8, 1.0)
                glVertex3f(x, y, z)
            glEnd()

        # Draw a small axis cross at the current walker position
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINES)
        size: float = 0.3
        # X axis line
        glVertex3f(-size, 0.0, 0.0)
        glVertex3f(size, 0.0, 0.0)
        # Y axis line
        glVertex3f(0.0, -size, 0.0)
        glVertex3f(0.0, size, 0.0)
        # Z axis line
        glVertex3f(0.0, 0.0, -size)
        glVertex3f(0.0, 0.0, size)
        glEnd()
        glPopMatrix()

# Global variables (annotated)
walker: Optional[RandomWalker3D] = None
rotation_angle: float = 0.0

def init() -> None:
    """Initialize global OpenGL state used by the scene."""
    glClearColor(0.0, 0.0, 0.0, 1.0)  # black background
    glEnable(GL_DEPTH_TEST)  # enable depth buffering
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # alpha blending
    glEnable(GL_LINE_SMOOTH)  # nicer lines
    glLineWidth(2.0)

def setup_projection(width: int, height: int) -> None:
    """Configure the projection matrix and viewport.

    Args:
        width: Framebuffer width in pixels.
        height: Framebuffer height in pixels.
    """
    if height == 0:
        height = 1

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Use a perspective projection (fov, aspect, near, far)
    gluPerspective(45.0, width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def reshape(window: Any, width: int, height: int) -> None:
    """GLFW framebuffer size callback -- update projection on resize."""
    setup_projection(width, height)

def display() -> None:
    """Render one frame of the scene (camera, grid, axes, and walker)."""
    global walker, rotation_angle

    # Clear both color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Simple orbiting camera looking at the origin
    gluLookAt(30.0, 30.0, 30.0,  # eye position
              0.0, 0.0, 0.0,     # look-at point
              0.0, 1.0, 0.0)     # up vector

    # Slowly rotate the entire scene around the Y axis
    glRotatef(rotation_angle, 0.0, 1.0, 0.0)
    rotation_angle += 0.5

    # Draw a ground grid for spatial reference
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_LINES)
    for i in range(-20, 21, 2):
        glVertex3f(float(i), 0.0, -20.0)
        glVertex3f(float(i), 0.0, 20.0)
        glVertex3f(-20.0, 0.0, float(i))
        glVertex3f(20.0, 0.0, float(i))
    glEnd()

    # Draw world axes (X=red, Y=green, Z=blue)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(10.0, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 10.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 10.0)
    glEnd()

    # Safely draw the walker if it has been initialized
    if walker is not None:
        walker.display()

def main() -> None:
    """Entry point: initialize GLFW and run the main render loop."""
    global walker

    # Initialize GLFW
    if not glfw.init():
        print("ERROR: Failed to initialize GLFW")
        sys.exit(1)

    # Create window (width, height, title)
    window = glfw.create_window(800, 600, "3D Random Walker", None, None)
    if not window:
        print("ERROR: Failed to create GLFW window")
        glfw.terminate()
        sys.exit(1)

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, reshape)

    # Initialize OpenGL state
    init()

    # IMPORTANT: Setup projection matrix manually on startup
    width, height = glfw.get_framebuffer_size(window)
    setup_projection(width, height)

    # Initialize walker instance
    walker = RandomWalker3D()

    print("Window created successfully. Starting render loop...")
    print(f"Initial framebuffer size: {width}x{height}")

    # Main render loop until the user closes the window
    while not glfw.window_should_close(window):
        walker.step()
        display()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()