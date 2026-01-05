from p5 import *
class Ball:
    def __init__(self, x, y, radius):
        self.position = Vector(x, y)
        self.velocity = Vector(4, 3)
        self.radius = radius
        self.gravity = Vector(0, 0.2)
        self.damping = 0.9
        
    def update(self):
        # Apply gravity and update position
        self.velocity.add(self.gravity)
        self.position.add(self.velocity)
        
    def check_edges(self, width, height):
        # Check horizontal boundaries
        if self.position.x > width - self.radius:
            self.position.x = width - self.radius
            self.velocity.x *= -1
        elif self.position.x < self.radius:
            self.position.x = self.radius
            self.velocity.x *= -1
            
        # Check vertical boundaries
        if self.position.y > height - self.radius:
            self.position.y = height - self.radius
            self.velocity.y *= -self.damping
            
    def display(self):
        fill(255, 0, 0)  # Red color
        no_stroke()
        circle((self.position.x, self.position.y), self.radius * 2)

class BouncingBallSketch:
    def __init__(self, width=600, height=400):
        self.width = width
        self.height = height
        self.ball = None
        
    def setup(self):
        size(self.width, self.height)
        title("Bouncing Ball - Processing-Python (OOP)")
        self.ball = Ball(self.width/2, self.height/2, 20)
        
    def draw(self):
        background(255)  # White background
        
        self.ball.update()
        self.ball.check_edges(self.width, self.height)
        self.ball.display()

# Create and run the sketch
sketch = BouncingBallSketch()
        
def setup():
    sketch.setup()
    
def draw():
    sketch.draw()

# Run the sketch
if __name__ == '__main__':
    run()
