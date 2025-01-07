import pyglet
from typing import Optional, Callable, Any, get_args

class Player(pyglet.window.Window):
    def __init__(self,
                 frame_generator: Callable[[Any, float], Any], 
                 fps_max: int = 30,
                 fps_display: bool = False,
                 mouse_sensitivity: float = 1.0,
                 **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.frame_generator: Callable = frame_generator
        self.keyboard_state = pyglet.window.key.KeyStateHandler()
        self.mouse_state = pyglet.window.mouse.MouseStateHandler()
        self.mouse_movement = { 'dx': 0, 'dy': 0 }
        self._previous_mouse_x: int = 0
        self._previous_mouse_y: int = 0
        self.mouse_sensitivity: float = mouse_sensitivity
        self.fps_max: float = fps_max
        if fps_display:
            self.fps_display = pyglet.window.FPSDisplay(window=self, samples=10)
        else:
            self.fps_display = None

        self.push_handlers(self.keyboard_state)
        self.push_handlers(self.mouse_state)
        
        # Set up the sprite for frame display
        self.sprite: Optional[pyglet.sprite.Sprite] = None

        # Schedule the update function
        pyglet.clock.schedule_interval(self.update, 1.0/fps_max)

    def render_frame(self, frame: Any) -> None:
        # Convert numpy array to pyglet image
        height, width = frame.shape[:2]
        img = pyglet.image.ImageData(width, height, 'RGB', frame.tobytes())
        scale_x = self.width / width
        scale_y = self.height / height
        # Create or update sprite
        if self.sprite:
            self.sprite.delete()
        self.sprite = pyglet.sprite.Sprite(img)
        self.sprite.scale = min(scale_x, scale_y)

    def on_draw(self) -> None:
        self.clear()
        if self.sprite:
            self.sprite.draw()
        if self.fps_display:
            self.fps_display.draw()

    def update(self, dt: float) -> None:
        # Calculate mouse movement between frames
        self.mouse_movement['dx'] = (self._mouse_x - self._previous_mouse_x) * self.mouse_sensitivity
        self.mouse_movement['dy'] = (self._mouse_y - self._previous_mouse_y) * self.mouse_sensitivity
        self._previous_mouse_x = self._mouse_x
        self._previous_mouse_y = self._mouse_y

        frame = self.frame_generator(self, dt)
        if frame is None:
            pyglet.app.exit()
            return
        
        self.render_frame(frame)

    def run(self) -> bool:
        self.activate()
        pyglet.app.run()
        return False