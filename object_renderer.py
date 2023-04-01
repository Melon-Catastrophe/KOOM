import arcade
import math     # For sqrt() and temporary ceil()
from PIL import Image       # For image opening, cropping
from PIL import ImageOps    # For image scaling
from ray import *

class Object_Renderer():
    def __init__(self, settings):
        self.settings = settings
        self.width_divisions = self.settings.width_divisions
        self.objects = []
        self.heights = []
        self.max_height = self.settings.screen_height / 2

        # Using Pythagorean's Theorem to determine the maximum length of a ray. This will change if the map changes.
        max_ray_height = self.settings.screen_height - (self.settings.tile_size * 2)
        max_ray_width = self.settings.screen_width - (self.settings.tile_size * 2)
        self.max_ray_length = math.sqrt(max_ray_height**2 + max_ray_width**2)

    def update(self, rays):
        self.objects = rays
        self.heights = []

        # TODO: See if there is a way to make a separate heights list in RayCaster that is more efficient.
        for ray in self.objects:
            self.heights.append(ray.get_distance())

        # Normalize from 0 to 1.
        self._normalize_heights()

        #   It is important to note that before the following loop is run, the values in self.heights are in a range from
        # 0 to 1, 0 representing the smallest ray distance and 1 representing the largest possible ray distance. We want
        # to change these values to make a large height for close objects, and small wall heights for far away objects.
        #   We do this by first, setting self.heights[i] to "1 - itself" to make the small values higher and vice versa.
        #   Next, we multiply the new height value by the maximumm height of the screen. Now the values in self.heights
        # are actually heights.
        for i_height in range(len(self.heights)):
            normalized_height_value = self.heights[i_height]
            assert normalized_height_value >= 0
            assert normalized_height_value <= 1
            
            normalized_height_value = 1 - normalized_height_value
            height = normalized_height_value * self.max_height
            self.heights[i_height] = height

    def render(self):
        # TODO: Do a test to see if it is faster to have a list of textures or to create all of the textures here.
        width = self.width_divisions
        center_y = self.settings.screen_height / 2
        for i_height in range(len(self.heights)):
            center_x = (self.width_divisions * i_height) + (self.width_divisions / 2)
            
            if self.settings.use_textures:
                texture = self._get_wall_texture(i_height, center_x)
                texture.draw_scaled(center_x, center_y)
            else:
                color_value = self._get_color_value_for_y_coord(self.objects[i_height].get_end_y())
                gray_color = (color_value, color_value, color_value)
                arcade.draw_rectangle_filled(center_x, center_y, width, self.heights[i_height], gray_color)

        # image = Image.open("resources/images/brick_texture_256.jpg")
        # image.putalpha(150)
        # tex = arcade.Texture("fdsa", image)
        # tex.draw_scaled(image.width / 2, self.settings.screen_height / 2)



    def _normalize_heights(self):
        """""""""""""""""""""""""""""
        NORMALIZE HEIGHTS
        This function uses the maximum possible length of a ray (the map's diagonal) and the minimum possible length 
        of a ray (0) to normalize all of the values within self.heights to be between 0 and 1. After heights are normalized,
        we can then multiply them by the tallest value we would like for each rectangle (the screen height) to get the 
        heights of our rectangles we will draw.
        """""""""""""""""""""""""""""
        max_value = self.max_ray_length
        min_value = 0

        for i_height in range(len(self.heights)):
            height = (self.heights[i_height] - min_value) / (max_value - min_value)
            self.heights[i_height] = height
            assert height > 0

    def _get_wall_texture(self, height_index, x_offset, image_path="resources/images/brick_texture_256.jpg"):
        img = Image.open(image_path)

        x_offset = int(x_offset)
        # Preparing for PIL. PIL cannot use floats for cropping and fitting.
        left = int(x_offset - math.floor(self.width_divisions / 2))
        right = int(x_offset + math.ceil(self.width_divisions / 2))

        img_1 = None
        img_2 = None
        if (right) > img.width:
            img_2 = Image.open(image_path)
            img_1 = img
            extra_x = (x_offset + (right - left)) - img.width
            # print("X_offset:", x_offset)
            # print("Left:", left)
            # print("Right:", right)
            # print("Extra: ", extra_x, "\n")
            img_1.crop((left, 0, x_offset, img_1.height))
            img_2.crop((0, 0, extra_x, img_2.height))
            img = Image.new("RGBA", (self.width_divisions, img_1.height))   # Replacing self.width_divisions here with img_1.width + img_2.width results in strange behavior.
            img.paste(img_1)
            img.paste(img_2, (img_1.width, 0))
            
        else:
            img = img.crop((left, 0, right, img.height))
        img = ImageOps.fit(img, (img.width, int(self.heights[height_index])))

        return arcade.Texture(str(height_index), img)

    def _get_color_value_for_y_coord(self, y_coordinate):
        max_value = self.settings.screen_height - self.settings.tile_size
        min_value = self.settings.tile_size

        normalized_y_coord = (y_coordinate - min_value) / (max_value - min_value)

        # We want the color value to be between 75 and 175
        color_value = normalized_y_coord * 100
        color_value += 75
        return color_value

    def _get_texture_offset(self, ray_index):
        end_position = self.objects[ray_index].endPos
        
        if self._is_on_vertical(end_position):
            return end_position.y % self.settings.tile_size
        elif self._is_on_horizontal(end_position):
            return end_position.x % self.settings.tile_size
        else:
            assert False, "The end position of the rays do not coincide with the tile sizes like they should."

    def _is_on_vertical(self, position):
        if position.x % self.settings.tile_size == 0:
            return True
        else:
            return False
        
    def _is_on_horizontal(self, position):
        if position.y % self.settings.tile_size == 0:
            return True
        else:
            return False