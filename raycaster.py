import arcade
import math         # for converting deg -> radians and angle things
from ray import *

class Raycaster(arcade.Sprite):
    def __init__(self):
        self._rays = []
        self._objects_hit = []
        super().__init__()

    """""""""""""""""""""""
    UPDATE
    Updates the raycaster. Casts rays throughout the field of view of the player, which is set in setting.json.
    The total amount of rays desired is equal to 1/4 of the screen width in our case.
    We could also put a ray_counter in the while loop, and increment that so our while condition could be while 
    ray_counter <= total_rays.
    """""""""""""""""""""""
    def update(self, game, width_divisions=10):
        self._follow_player(game.player)
        self._rays = []

        total_rays = game.settings.screen_width / width_divisions
        step_amount = game.settings.fov / total_rays
        half_fov = game.settings.fov / 2
        ray_angle = -1 * (half_fov)
        
        while ray_angle <= half_fov:
            self._cast_ray(ray_angle, game)
            ray_angle += step_amount

    """""""""""""""""""""""
    CAST RAY
    Each time this function is called, it casts a ray at an angle specified that is offset from Raycaster's angle.
    It does that by scanning the horizontal and vertical lines every tile_size width for collisions. The Raycaster will
    keep the shortest ray.
    """""""""""""""""""""""
    def _cast_ray(self, local_angle_deg, game):
        total_angle = self._normalize_angle(self.angle + local_angle_deg)

        self._x_intercepts = self._get_x_intercepts()
        self._y_intercepts = self._get_y_intercepts()
        self._quadrant = self._get_quadrant(total_angle)
        self._slope = self._get_slope_from_angle_deg(total_angle)
        
        found_x_collision = False
        found_y_collision = False

        x_collision = arcade.Sprite("resources\images\pointer.png")
        x_collision.center_x, x_collision.center_y, found_x_collision = self._find_x_collision_point(game)

        y_collision = arcade.Sprite("resources\images\pointer.png")
        y_collision.center_x, y_collision.center_y, found_y_collision = self._find_y_collision_point(game)

        pointer = arcade.Sprite("resources\images\pointer.png")

        # Find the shortest ray collision and append that ray to self._rays.
        if found_x_collision and found_y_collision:
            dist_x_collision = abs(arcade.get_distance(self.center_x, self.center_y, x_collision.center_x, x_collision.center_y))
            dist_y_collision = abs(arcade.get_distance(self.center_x, self.center_y, y_collision.center_x, y_collision.center_y))

            if dist_x_collision < dist_y_collision:
                pointer = x_collision
            else:
                pointer = y_collision
        elif found_x_collision:
            pointer = x_collision
        elif found_y_collision:
            pointer = y_collision
        elif not found_x_collision and not found_y_collision:
            pointer = x_collision       # Chose x_collision at random. They should point in a visually similar way.
            # assert False, "A ray found a way outside of the map. Ensure map is fully enclosed."
        else:
            assert False, "Should be a 0% chance that this assert fires."
        
        startPos = Vec2(self.center_x, self.center_y)
        endPos = Vec2(pointer.center_x, pointer.center_y)
        diffPos = Vec2(endPos.x - startPos.x, endPos.y - startPos.y)
        calcAngle = self._normalize_angle(math.degrees(math.atan2(diffPos.x, diffPos.y)))
        assert self.close_enough(calcAngle, total_angle, 0.01), "Starting angle and ending angle of ray do not match."

        ray = Ray(startPos, endPos)
        self._rays.append(ray)

    def _find_x_collision_point(self, game):
        pointer = arcade.Sprite("resources\images\pointer.png")
        pointer.center_x = self.center_x
        pointer.center_y = self.center_y

        # Finding vertical line wall collisions below.
        # If ray is pointed in a positive x direction...
        closest_vertical_x_index = int(pointer.center_x // 32)
        assert self.center_x == pointer.center_x
        assert self.center_y == pointer.center_y
        if self._quadrant == 1 or self._quadrant == 2:
            closest_vertical_x_index += 1
            assert self._x_intercepts[closest_vertical_x_index] > pointer.center_x
            assert closest_vertical_x_index == int(pointer.center_x // 32) + 1
        else:
            assert self._x_intercepts[closest_vertical_x_index] < pointer.center_x
            assert closest_vertical_x_index == int(pointer.center_x // 32)
        
        pointer.center_x = self._x_intercepts[closest_vertical_x_index]
        pointer.center_y = self._get_y_from_x(self.center_x, self.center_y, self._slope, pointer.center_x)
        if self._quadrant == 1 or self._quadrant == 2:
            assert pointer.center_x > self.center_x
        else:
            assert pointer.center_x <= self.center_x

        dx = game.settings.tile_size
        if self._quadrant == 3 or self._quadrant == 4:
            dx *= -1
        dy = self._slope * dx

        found_x_collision = False
        while not found_x_collision and not self._is_offscreen(game.settings, pointer.center_x, pointer.center_y):
            if arcade.check_for_collision_with_list(pointer, game.map.scene["Walls"]):
                found_x_collision = True
            else:
                pointer.center_x += dx
                pointer.center_y += dy

        return pointer.center_x, pointer.center_y, found_x_collision

    def _find_y_collision_point(self, game):
            pointer = arcade.Sprite("resources\images\pointer.png")
            pointer.center_x = self.center_x
            pointer.center_y = self.center_y

            closest_horizontal_y_index = int(pointer.center_y // 32)
            if self._quadrant == 1 or self._quadrant == 4:
                closest_horizontal_y_index += 1
                assert self._y_intercepts[closest_horizontal_y_index] > pointer.center_y
            else:
                assert self._y_intercepts[closest_horizontal_y_index] <= pointer.center_y
            
            pointer.center_y = self._y_intercepts[closest_horizontal_y_index]
            pointer.center_x = self._get_x_from_y(self.center_x, self.center_y, self._slope, pointer.center_y)
            
            dy = game.settings.tile_size
            if self._quadrant == 2 or self._quadrant == 3:
                dy *= -1
            
            dx = dy / self._slope

            found_y_collision = False
            while not found_y_collision and not self._is_offscreen(game.settings, pointer.center_x, pointer.center_y):
                if arcade.check_for_collision_with_list(pointer, game.map.scene["Walls"]):
                    found_y_collision = True
                else:
                    pointer.center_x += dx
                    pointer.center_y += dy

            return pointer.center_x, pointer.center_y, found_y_collision

    def close_enough(self, value, test, tolerance):
        difference = value - test
        return (difference >= -tolerance) and (difference <= tolerance)

    def draw_rays(self):
        for ray in self._rays:
            ray.draw()

    def get_rays(self):
        return self._rays

    def _get_quadrant(self, angle_degrees):
        if angle_degrees >= 0 and angle_degrees <= 90:
            return 1
        elif angle_degrees > 90 and angle_degrees <= 180:
            return 2
        elif angle_degrees > 180 and angle_degrees <= 270:
            return 3
        elif angle_degrees > 270 and angle_degrees < 360:
            return 4
        else: 
            assert False
    
    def _get_x_from_y(self, x1, y1, m, y2):
        # y1-y2 = m * (x1-x2)
        # (y1-y2) / m = x1 - x2
        # ((y1-y2) / m) - x1 = -x2
        # (((y1-y2) / m) - x1) * -1 = x2
        return (((y1-y2) / m) - x1) * -1
        # TODO: do testing for this function

    def _get_y_from_x(self, x1, y1, m, x2):
        # -y2 = m * (x1-x2) - y1
        # y2 = (m * (x1-x2) - y1) * -1
        return (m * (x1-x2) - y1) * -1

    def _get_x_intercepts(self):
        return [0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, \
            480, 512, 544, 576, 608, 640, 672, 704, 736, 768, 800]

    def _get_y_intercepts(self):
        return [0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448]

    def _get_slope_from_angle_deg(self, angle_degrees):
        try:
            return 1/(math.tan(math.radians(angle_degrees)))
        except ZeroDivisionError:
            return 1/(math.tan(math.radians(angle_degrees)) + 0.00000000000001)
        
    def _get_slope_from_angle_rad(self, angle_radians):
        try:
            return 1/(math.tan(angle_radians))
        except ZeroDivisionError:
            return 1/(math.tan(angle_radians) + 0.00000000000001)

    def _follow_player(self, player):
        self.center_x = player.center_x
        self.center_y = player.center_y
        self.angle = player.angle

    def _is_offscreen(self, settings, x, y):
        return x >= settings.screen_width or x < 0 or y >= settings.screen_height or y < 0

    # TODO: Move this somewhere else to reduce redundancy.
    def _normalize_angle(self, angle_degrees):
        while angle_degrees >= 360:
            angle_degrees -= 360
        while angle_degrees < 0:
            angle_degrees += 360

        return angle_degrees