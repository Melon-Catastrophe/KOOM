import json

class Settings():
    def __init__(self, settings_filename):
        self.settings_filename = settings_filename
        self.is_testing = False
        self.fps = None
        self.screen_height = None
        self.screen_width = None
        self.title = None
        self.tile_scaling = None
        self.width_divisions = None

    ##############################################
    # LOAD SETTINGS
    # Given a game, this will load the settings into the game as a dictionary.
    ###############################################
    def load_settings(self):
        with open(self.settings_filename, 'r') as json_file:
            if not self.is_testing:
                settings = json.load(json_file)
                self.fps = settings["fps"]
                self.screen_height = settings["screen_height"]
                self.screen_width = settings["screen_width"]
                self.title = settings["title"]
                self.tile_scaling = settings["tile_scaling"]
                self.tile_size = settings["tile_size"]
                self.player_speed = settings["player_speed"]
                self.player_turn_speed = settings["player_turn_speed"]
                self.fov = settings["FOV"]
                self.width_divisions = settings["width_divisions"]
                self.use_textures = settings["use_textures"]
            else:
                self.settings = json.load(json_file)

# ###############################################
# # GENERATE SETTINGS
# # This is to be used only by this file. Generates sample settings.
# # This function will be commented when we do not want to give game access.
# ###############################################
# def _generate_settings_file():
#     settings = {
#         "fps": "30",
#         "screen_width": 800,
#         "screen_height": 450,
#     }

#     with open('settings.json', 'w') as json_file:
#         json.dump(settings, json_file, indent=4, sort_keys=True)

# _generate_settings_file()