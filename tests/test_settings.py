import sys
sys.path.append('..\\')
from settings import *

class Test_Settings():
    def __init__(self):
        pass

    def run(self):
        self.load_basicTest

    def load_basicTest(self):
        # Setup
        settings = Settings("")
        settings.settings_filename = "settings_test.json"
        settings.is_testing = True

        # Exercise
        settings.load_settings()
        
        # Verify
        assert settings.settings["number"] == 10
        assert settings.settings["boolean"] == True
        assert settings.settings["string"] == "string"