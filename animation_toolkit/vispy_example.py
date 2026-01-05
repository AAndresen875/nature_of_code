"""vispy_example.py

Random walkers demo using VisPy with the GLFW backend.

This module configures the GLFW backend early (required by some systems),
initializes a small particle system of random walkers, and animates them
using GLSL shaders via VisPy's gloo.Program.
"""

import os
os.environ['DISPLAY'] = ':0'

# CRITICAL: Force GLFW backend BEFORE importing other vispy modules
from vispy import app
app.use_app('glfw')

import numpy as np
from typing import Any
from vispy import gloo
from vispy.gloo import Program

# Vertex shader
vertex = """
attribute vec2 position;
attribute vec3 color;
varying vec3 v_color;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
    gl_PointSize = 5.0;
    v_color = color;
}
"""

# Fragment shader
fragment = """
varying vec3 v_color;
void main() {
    gl_FragColor = vec4(v_color, 1.0);
}
"""

class Canvas(app.Canvas):
    """VisPy Canvas that renders random walkers using a GLSL program.

    The canvas manages positions, colors, and a timer to update the
    walkers each frame.
    """

    def __init__(self) -> None:
        """Initialize the canvas, GLSL program, and animation timer."""
        # Call parent constructor and set up window properties
        app.Canvas.__init__(
            self,
            size=(800, 600),
            title='Random Walkers - GLFW Backend',
            keys='interactive',
            position=(100, 100),
        )

        # Initialize walkers
        self.n_walkers: int = 100
        self.positions: np.ndarray = np.random.uniform(-0.5, 0.5, (self.n_walkers, 2)).astype(np.float32)
        self.colors: np.ndarray = np.random.uniform(0.0, 1.0, (self.n_walkers, 3)).astype(np.float32)

        # Create GLSL program and bind initial buffers
        self.program: Program = Program(vertex, fragment)
        self.program['position'] = self.positions
        self.program['color'] = self.colors

        # Set up timer for animation; 'auto' uses the best available timer
        self.timer: app.Timer = app.Timer('auto', connect=self.on_timer, start=True)

        # Clear color and display settings
        gloo.set_clear_color('black')

        # Explicitly show the window (some platforms require this)
        self.show()

        print(f"Canvas created with backend: {app.use_app().backend_name}")
        print(f"Window size: {self.size}")
    
    def on_draw(self, event: Any) -> None:
        """Draw callback invoked by VisPy when the canvas needs repainting.

        Args:
            event: Event object provided by VisPy (unused).
        """
        gloo.clear()
        # Draw points using the GLSL program
        self.program.draw('points')

    def on_resize(self, event: Any) -> None:
        """Handle resize events by updating the GL viewport."""
        # event.physical_size gives the actual framebuffer size in pixels
        gloo.set_viewport(0, 0, *event.physical_size)

    def on_timer(self, event: Any) -> None:
        """Timer callback to step the random walkers and schedule a redraw."""
        # Random small displacement for each walker
        step: np.ndarray = np.random.uniform(-0.01, 0.01, (self.n_walkers, 2)).astype(np.float32)
        self.positions += step

        # Clip positions to normalized device coordinates [-1, 1]
        self.positions = np.clip(self.positions, -1.0, 1.0)

        # Upload updated positions to the GPU and request redraw
        self.program['position'] = self.positions
        self.update()

if __name__ == '__main__':
    print(f"Using vispy backend: {app.use_app().backend_name}")
    # Create and run the canvas
    canvas: Canvas = Canvas()
    print("Random walkers running. Close window or press Ctrl+C to exit.")
    app.run()
