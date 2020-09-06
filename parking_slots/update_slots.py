#!/usr/bin/env python3
from ultrasonic import Ultrasonic
import requests
import time

ECHO_0_PIN = 3
TRIG_0_PIN = 5

ECHO_1_PIN = 7
TRIG_1_PIN = 11

ECHO_2_PIN = 13
TRIG_2_PIN = 15

ECHO_3_PIN = 16
TRIG_3_PIN = 17

s0 = Ultrasonic(echo=ECHO_0_PIN, trigger=TRIG_0_PIN)
s1 = Ultrasonic(echo=ECHO_1_PIN, trigger=TRIG_1_PIN)
s2 = Ultrasonic(echo=ECHO_2_PIN, trigger=TRIG_2_PIN)
s3 = Ultrasonic(echo=ECHO_3_PIN, trigger=TRIG_3_PIN)


def sensors_state():
    try:
        data = {
            "A0": s0.detected(),
            "A1": s1.detected(),
            "A2": s2.detected(),
            "A3": s3.detected()
        }
        requests.get("http://127.0.0.1:5000/update_slot", json=data)
    except:
        print("Connection ERROR!!!")
    
if __name__ == "__main__":
    try:
        while True:
            sensors_state()
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopped!!!")
    

