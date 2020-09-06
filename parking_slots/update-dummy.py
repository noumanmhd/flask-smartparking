#!/usr/bin/env python3
import requests

def sensors_state():
    try:
        data = {
            "A0": False,
            "A1": True,
            "A2": False,
            "A3": True
        }
        requests.get("http://127.0.0.1:5000/update_slot", json=data)
    except:
        print("Connection ERROR!!!")

sensors_state()
    
    

