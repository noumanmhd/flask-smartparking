from gpiozero import DistanceSensor
import time
 
LIMIT = 4

class Ultrasonic(object):
    def __init__(self,echo= 24, trigger=18):
        self.sensor = DistanceSensor(echo=echo, trigger=trigger)
    
    def detected(self):
        if (self.sensor.distance) < LIMIT:
            return True
        return False

