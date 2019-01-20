# Class represent moving battery-vehicle with average speed, battery life and charging time
class Vehicle:
    def __init__(self, speed,  battery_life, charging_time):
        self.speed = speed
        self.battery_life = battery_life
        self.charging_time = charging_time
