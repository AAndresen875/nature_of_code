import numpy as np
from vispy import app, gloo
from vispy.gloo import Program

# Vertex shader - processes each vertex position
vertex_shader = """
attribute vec2 a_position;
attribute vec3 a_color;
varying vec3 v_color;

void main() {
    gl_Position = vec4(a_position, 0.0, 1.0);
    gl_PointSize = 5.0;
    v_color = a_color;
}
"""

# Fragment shader - determines pixel colors
fragment_shader = """
varying vec3 v_color;

void main() {
    gl_FragColor = vec4(v_color, 1.0);
}
"""

class RandomWalkerCanvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, size=(800, 600), title='Random Walkers',
                           keys='interactive')
        
        # Number of walkers
        self.n_walkers = 100
        
        # Initialize positions (start at center)
        self.positions = np.zeros((self.n_walkers, 2), dtype=np.float32)
        
        # Random colors for each walker
        self.colors = np.random.uniform(0.3, 1.0, (self.n_walkers, 3)).astype(np.float32)
        
        # Create shader program
        self.program = Program(vertex_shader, fragment_shader)
        self.program['a_position'] = self.positions
        self.program['a_color'] = self.colors
        
        # Set background color
        gloo.set_clear_color('black')
        gloo.set_state('translucent')
        
        # Start timer for animation (60 FPS)
        self._timer = app.Timer('auto', connect=self.on_timer, start=True)
        
        self.show()
    
    def on_draw(self, event):
        gloo.clear()
        self.program.draw('points')
    
    def on_timer(self, event):
        # Random walk: add random step to each position
        step_size = 0.02
        steps = np.random.uniform(-step_size, step_size, (self.n_walkers, 2))
        self.positions += steps.astype(np.float32)
        
        # Wrap around screen edges
        self.positions = np.clip(self.positions, -1.0, 1.0)
        
        # Update positions in GPU
        self.program['a_position'] = self.positions
        
        # Trigger redraw
        self.update()
    
    def on_resize(self, event):
        gloo.set_viewport(0, 0, *event.physical_size)

if __name__ == '__main__':
    canvas = RandomWalkerCanvas()
    app.run()
