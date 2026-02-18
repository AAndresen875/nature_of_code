"""
Docstring for src.base_canvas

This module provides the BaseCanvas class, which serves as a foundational canvas for drawing operations.
It handles the:
- Initialization of the canvas with specified width and height.
- loop management for continuous rendering.
- Basic event handling for user interactions.
"""

class BaseCanvas:
    """
    This is the base canvas class for drawing operations.
    It provides foundational methods and properties to handle the:
    * canvas setup, 
    * the loop, 
    * basic event handling.
    * aesthetics.
    """
    
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.is_running = False

    def start_loop(self):
        """Start the drawing loop."""
        self.is_running = True
        while self.is_running:
            self.draw()

    def stop_loop(self):
        """Stop the drawing loop."""
        self.is_running = False

    def draw(self):
        """Placeholder for drawing logic."""
        pass