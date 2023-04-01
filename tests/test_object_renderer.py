import sys
import os
from PIL import Image

sys.path.append('.\\')
from object_renderer import *

class Fake_Settings():
    def __init__(self, width_divisions):
        self.width_divisions = width_divisions
        self.screen_height = 100
        self.screen_width = 100
        self.tile_size = 0

class Test_Object_Renderer():
    def __init__(self):
        pass

    def run(self):
        self.getWallTexture_evenWidthDivisions()
        self.getWallTexture_oddWidthDivisions()

    def getWallTexture_evenWidthDivisions(self):
        # Setup
        settings = Fake_Settings(width_divisions=2)
        renderer = Object_Renderer(settings)
        renderer.settings = settings
        renderer.width_divisions = renderer.settings.width_divisions
        renderer.objects = 0
        renderer.heights = [8]
        renderer.max_height = 0
        
        texture = None
        height_index = 0
        x_offset = 5

        result_test = Image.open("tests\\test_get_texture_result_even.png")

        # Exercise
        texture = renderer._get_wall_texture(height_index, x_offset, image_path="tests\\test_get_texture.png")

        # Verify
        assert texture.width == 2
        assert texture.height == 8
        assert list(texture.image.getdata()) == list(result_test.getdata())

        # Teardown

    def getWallTexture_oddWidthDivisions(self):
        # Setup
        settings = Fake_Settings(width_divisions=3)
        renderer = Object_Renderer(settings)
        renderer.settings = settings
        renderer.width_divisions = renderer.settings.width_divisions
        renderer.objects = 0
        renderer.heights = [8]
        renderer.max_height = 0
        
        texture = None
        height_index = 0
        x_offset = 5

        result_test = Image.open("tests\\test_get_texture_result_odd.png")

        # Exercise
        texture = renderer._get_wall_texture(height_index, x_offset, image_path="tests\\test_get_texture.png")

        # Verify
        assert texture.width == 3
        assert texture.height == 8
        assert list(texture.image.getdata()) == list(result_test.getdata())

        # Teardown

        