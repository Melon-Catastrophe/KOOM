import sys  # For help with importing specific file paths.

sys.path.append("tests")
from test_settings import *         # SETTINGS
from test_raycaster import *        # RAYCASTER
from test_object_renderer import *  # OBJECT RENDERER

class Test():
    def __init__(self):
        self._test_settings = Test_Settings()
        self._test_raycaster = Test_Raycaster()
        self._test_renderer = Test_Object_Renderer()

    def run(self):
        self._test_settings.run()
        self._test_raycaster.run()
        self._test_renderer.run()
        print("Tests pass!")