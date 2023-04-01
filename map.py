import arcade
import os

class Map():
    # I decided it would be easier to make Map from scratch than rely on Arcade's built-in tilemap editor.
    def __init__(self, game):
        # # Lets us use relative file paths.
        # file_path = os.path.dirname(os.path.abspath(__file__))
        # os.chdir(file_path)

        self.filename = "resources\maps\level01.tmx"
        self.load_map(game)

    def load_map(self, game):
        # Spatial hashing speeds up collisions, but slows movement of a sprite.
        layer_options = {
            "Walls": {
                "use_spatial_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(self.filename, game.settings.tile_scaling, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.wall_physics = arcade.PhysicsEngineSimple(game.player, self.scene["Walls"])
        
    def draw(self):
        self.scene.draw()

    def update(self):
        self.wall_physics.update()



    # def __init__(self):
    #     self.object_locations = [
    #         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    #     ]

    # def draw(self, game):
    #     for row in range(len(self.object_locations)):
    #         if row == 0:
    #             assert self.object_locations[row] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    #         for col in range(len(self.object_locations[row])):
    #             if self.object_locations[row][col] == 1:
    #                 center_x, center_y = self._convert_map_coord_to_screen_coord(game, col, row)    # I think row and col should be switched here, but this makes it draw properly.
    #                 arcade.draw_rectangle_outline(center_x, center_y, game.settings.tile_size, game.settings.tile_size, arcade.color.WHITE)

    # def _convert_map_coord_to_screen_coord(self, game, row, col):
    #     tile_multiplier = game.settings.tile_size
    #     half_tile_width = tile_multiplier / 2

    #     row_center_tile = (row * tile_multiplier) + half_tile_width
    #     col_center_tile = (col * tile_multiplier) + half_tile_width
    #     return row_center_tile, col_center_tile