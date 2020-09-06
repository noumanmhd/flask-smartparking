#!/usr/bin/env python3
import requests


try:
    data = {
        "results": ["ajhj19", "jhdsauh", "jshuf"]
    }
    r = requests.get("http://127.0.0.1:5000/get_plate", json=data)
    print(r.status_code)
except:
    print("Connection ERROR!!!")

