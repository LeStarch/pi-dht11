#!/usr/bin/env python3
from sensor.dht11 import HTSensor,ReadError
yolo = HTSensor(29)
try:
    humidity, temperature = yolo.read()
    print("Humidity:",humidity,"Temperature:",temperature)
except ReadError:
    print("Read failed")
finally:
    yolo.cleanup()
