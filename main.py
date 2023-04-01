import arcade

from map import *
from player import *
from settings import *
from test import *
from raycaster import *
from object_renderer import *

class Game(arcade.Window):   
    def __init__(self):
        settings_filename = "resources\settings.json"
        self.settings = Settings(settings_filename)
        self.settings.load_settings()
        super().__init__(self.settings.screen_width, self.settings.screen_height, self.settings.title, center_window=True)

        self.player = None
        self.map = None
        self.raycaster = None
        self.object_renderer = None

    def setup(self):
        self.player = Player(self)
        self.map = Map(self)
        self.raycaster = Raycaster()
        self.object_renderer = Object_Renderer(self.settings)

    def on_draw(self):
        self.clear()
        # self.map.draw()
        # self.raycaster.draw_rays()
        # self.player.draw()
        self.object_renderer.render()

        # Debugging information
        # arcade.draw_text("X: " + str(self.player.center_x), 40, self.settings.screen_height - 64)
        # arcade.draw_text("Y: " + str(self.player.center_y), 40, self.settings.screen_height - 80)
        # arcade.draw_text("Angle: " + str(self.player.angle), 40, self.settings.screen_height - 100)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.set_forward_motion(True)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.set_backward_motion(True)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.set_turn_left(True)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.set_turn_right(True)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.set_forward_motion(False)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.set_backward_motion(False)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.set_turn_left(False)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.set_turn_right(False)

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_update(self, delta_time):
        self.player.update()
        self.map.update()
        self.raycaster.update(self, width_divisions=self.settings.width_divisions)
        self.object_renderer.update(self.raycaster.get_rays())


def main():
    window = Game()
    window.setup()
    arcade.run()

if __name__ == '__main__':
    test = Test()
    test.run()

    main()