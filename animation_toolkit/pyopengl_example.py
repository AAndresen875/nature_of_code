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
from typing import List, Tuple

class RandomWalker3D:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.history: List[Tuple[float, float, float]] = [(0.0, 0.0, 0.0)]
        self.max_history = 500
        
    def step(self):
        step_size = 0.5
        direction = random.randint(0, 5)
        
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
        
        self.history.append((self.x, self.y, self.z))
        
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def display(self):
        if len(self.history) > 1:
            glBegin(GL_LINE_STRIP)
            for i, (x, y, z) in enumerate(self.history):
                fade = i / len(self.history)
                glColor3f(0.0, fade * 0.8, 1.0)
                glVertex3f(x, y, z)
            glEnd()
        
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINES)
        size = 0.3
        glVertex3f(-size, 0, 0)
        glVertex3f(size, 0, 0)
        glVertex3f(0, -size, 0)
        glVertex3f(0, size, 0)
        glVertex3f(0, 0, -size)
        glVertex3f(0, 0, size)
        glEnd()
        glPopMatrix()

# Global variables
walker = None
rotation_angle = 0.0

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glLineWidth(2.0)

def setup_projection(width, height):
    """Setup projection matrix"""
    if height == 0:
        height = 1
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def reshape(window, width, height):
    """Callback for window resize"""
    setup_projection(width, height)

def display():
    global walker, rotation_angle
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    gluLookAt(30.0, 30.0, 30.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)
    
    glRotatef(rotation_angle, 0.0, 1.0, 0.0)
    rotation_angle += 0.5
    
    # Draw grid
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_LINES)
    for i in range(-20, 21, 2):
        glVertex3f(i, 0, -20)
        glVertex3f(i, 0, 20)
        glVertex3f(-20, 0, i)
        glVertex3f(20, 0, i)
    glEnd()
    
    # Draw axes
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0, 0, 0)
    glVertex3f(10, 0, 0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 10, 0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 10)
    glEnd()
    
    walker.display()

def main():
    global walker
    
    # Initialize GLFW
    if not glfw.init():
        print("ERROR: Failed to initialize GLFW")
        sys.exit(1)
    
    # Create window
    window = glfw.create_window(800, 600, "3D Random Walker", None, None)
    if not window:
        print("ERROR: Failed to create GLFW window")
        glfw.terminate()
        sys.exit(1)
    
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, reshape)
    
    # Initialize OpenGL
    init()
    
    # IMPORTANT: Setup projection matrix manually on startup
    width, height = glfw.get_framebuffer_size(window)
    setup_projection(width, height)
    
    # Initialize walker
    walker = RandomWalker3D()
    
    print("Window created successfully. Starting render loop...")
    print(f"Initial framebuffer size: {width}x{height}")
    
    # Main loop
    while not glfw.window_should_close(window):
        walker.step()
        display()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main()