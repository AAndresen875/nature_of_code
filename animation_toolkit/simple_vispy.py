import os
os.environ['DISPLAY'] = ':0'

from vispy import app
import sys

# Enable verbose debugging
app.use_app(backend_name=None)  # Let vispy choose
print(f"Using backend: {app.use_app().backend_name}")

canvas = app.Canvas(size=(800, 600), title='Test Window')
print(f"Canvas native type: {type(canvas.native)}")
print(f"Canvas context: {canvas.context}")

canvas.show()
print("show() called")
print("Check Windows taskbar for 'Test Window'")

try:
    app.run()
except KeyboardInterrupt:
    print("Exiting...")
    sys.exit(0)