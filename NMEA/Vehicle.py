"""

This module provide Vehicle class to represent vehicle model
with speed, battery_life and charging time

"""


class Vehicle:
    def __init__(self, speed,  battery_life, charging_time=0):
        if charging_time < 0 or speed <= 0 or battery_life <= 0:
            raise ValueError("Values should be positive "
                             "(charging time should be 0 or positive)")
        self._speed = speed
        self._battery_life = battery_life
        self._charging_time = charging_time

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if value > 0:
            self._speed = value
        else:
            raise ValueError("Vehicle speed must be positive")

    @property
    def battery_life(self):
        return self._battery_life

    @battery_life.setter
    def battery_life(self, value):
        if value > 0:
            self._battery_life = value
        else:
            raise ValueError("Battery life speed must be positive")

    @property
    def charging_time(self):
        return self._charging_time

    @charging_time.setter
    def charging_time(self, value):
        if value >= 0:
            self._charging_time = value
        else:
            raise ValueError("Charging time speed must be positive or zero")
