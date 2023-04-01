import arcade
from math import sin, cos, radians

class Player(arcade.Sprite):
    def __init__(self, game):
        super().__init__()  # May remove this later if it causes problems.
        
        # Our variables are private.
        self._radius = 10
        self._color = arcade.color.LIME_GREEN
        self._speed = game.settings.player_speed
        self._angle_speed = game.settings.player_turn_speed
        self._is_motion_forward = False
        self._is_motion_back = False
        self._is_turn_left = False
        self._is_turn_right = False

        # Variables defined by arcade:Sprite are public.
        self.center_x = game.settings.screen_width / 2
        self.center_y = game.settings.screen_height / 2
        self.angle = 0      # Angle in degrees
        self.change_x = 0
        self.change_y = 0
        self.hit_box_algorithm = "Simple"
        self.set_hit_box([[-self._radius, 0], [0, self._radius], [self._radius, 0], [0, -self._radius]])        

    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, self._radius, self._color)

    def update(self):
        self.change_x = 0
        self.change_y = 0

        if self._is_motion_forward:
            self._move_forward()
        if self._is_motion_back:
            self._move_backward()
        if self._is_turn_left:
            self._turn_left()
        if self._is_turn_right:
            self._turn_right()

        self._normalize_angle()

    def _normalize_angle(self):
        while self.angle >= 360:
            self.angle -= 360
        while self.angle < 0:
            self.angle += 360

    def get_angle(self):
        return self.angle

    def _move_forward(self):
        change_x, change_y = self._get_changes() # Changes change_x and change_y.        

        # Move the player.
        self.center_x += change_x
        self.center_y += change_y
    
    def _move_backward(self):
        change_x, change_y = self._get_changes()

        # Move the player.
        self.center_x += -change_x
        self.center_y += -change_y

    def _get_changes(self):
        change_x = sin(radians(self.angle)) * self._speed
        change_y = cos(radians(self.angle)) * self._speed
        return change_x, change_y

    def _turn_left(self):
        self.angle -= self._angle_speed

    def _turn_right(self):
        self.angle += self._angle_speed

    def set_forward_motion(self, is_forward):
        self._is_motion_forward = is_forward

    def set_backward_motion(self, is_back):
        if self._is_motion_forward == True:
            self._is_motion_back = False
        else:
            self._is_motion_back = is_back

    def set_turn_left(self, is_left):
        self._is_turn_left = is_left

    def set_turn_right(self, is_right):
        self._is_turn_right = is_right