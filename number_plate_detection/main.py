#!/usr/bin/env python3
import cv2
import time
import requests
from gpiozero import Servo, AngularServo, Button
from detect import detect_image

SEROVO_0_PIN = 13
SEROVO_1_PIN = 19

IR_Sensor_0_PIN = 16
IR_Sensor_1_PIN = 20

camera = cv2.VideoCapture(0)

class Custom_Servo(object):
    def __init__(self, pin):
        self.pin = pin
        self.getValues()
        self.motor = AngularServo(self.pin, min_angle=self.min, max_angle=self.max)

    def getValues(self):
        s = Servo(self.pin)
        self.min = s.min() # measure the angle
        self.max = s.max() # measure the angle
    
    def open_servo(self):
        self.motor.max()
    
    def close_servo(self):
        time.sleep(3)
        self.motor.mid()

def check_plate(result):
    try:
        data = {
                "plats": result 
            }
        r = requests.get("http://127.0.0.1:5000/get_plate", json=data)
        if r.status_code == 200:
            return True
        return False
    except:
        return False

    
def capture():
    ret, img = camera.read()
    if ret:
        results = detect_image(img)
    if check_plate(results):
        m0.open_servo()  


if __name__ == "__main__":
    m0 = Custom_Servo(pin=SEROVO_0_PIN)
    s0 = Button(IR_Sensor_0_PIN,pull_up=False)
    s0.when_released = m0.close_servo

    m1 = Custom_Servo(pin=SEROVO_1_PIN)
    s1 = Button(IR_Sensor_1_PIN,pull_up=False)
    s1.when_pressed = m1.open_servo
    s1.when_released = m1.close_servo
    try:
        while True:
            capture()
    except KeyboardInterrupt:
        m0.close_servo
        m1.close_servo
        camera.release()


    
