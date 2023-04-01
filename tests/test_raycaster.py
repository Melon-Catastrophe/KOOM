import sys
sys.path.append('.\\')
from raycaster import *

def close_enough(value, test, tolerance):
    difference = value - test
    return (difference >= -tolerance) and (difference <= tolerance)

class Test_Raycaster():
    def __init__(self):
        pass

    def run(self):
        self.slopeFromDegrees_45()
        self.slopeFromDegrees_divide_by_zero()
        self.slopeFromDegrees_90()
        self.slopeFromRadians_45()
        self.slopeFromRadians_divide_by_zero()
        self.slopeFromRadians_90()

    def slopeFromDegrees_45(self):
        # Setup
        raycaster = Raycaster()
        angle = 45
        result = None

        # Exercise
        result = raycaster._get_slope_from_angle_deg(angle)

        # Verify
        assert close_enough(result, 1.0, 0.00001)

    def slopeFromDegrees_divide_by_zero(self):
        # Setup
        raycaster = Raycaster()
        angle = 0
        result = None

        # Exercise
        result = raycaster._get_slope_from_angle_deg(angle)

        # Verify
        assert True
        # If divide by zero condition did not trigger

    def slopeFromDegrees_90(self):
        # Setup
        raycaster = Raycaster()
        angle = 90
        result = None

        # Exercise
        result = raycaster._get_slope_from_angle_deg(angle)

        # Verify
        assert result < 1e10

    def slopeFromRadians_45(self):
        # Setup
        raycaster = Raycaster()
        angle = math.pi / 4
        result = None

        # Exercise
        result = raycaster._get_slope_from_angle_rad(angle)

        # Verify
        assert close_enough(result, 1.0, 0.00001)

    def slopeFromRadians_divide_by_zero(self):
        # Setup
        raycaster = Raycaster()
        angle = 0
        result = None

        # Exercise
        result = raycaster._get_slope_from_angle_rad(angle)

        # Verify
        assert True
        # If divide by zero condition did not trigger
    
    def slopeFromRadians_90(self):
        # Setup
        raycaster = Raycaster()
        angle = math.pi / 2
        result = None

        # Exercise
        result = raycaster._get_slope_from_angle_deg(angle)

        # Verify
        assert result < 1e10