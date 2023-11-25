import os
from time import sleep

import RPi.GPIO as GPIO

from constants import BATTERY_PIN, SHUTDOWN_NOW, START_RADIO_SERVICE, LOW_BATTERY_SFX, POLL_INTERVAL_IN_SEC
from soxplayer import SoxPlayer

radio = SoxPlayer()
GPIO.setmode(GPIO.BCM)
GPIO.setup(BATTERY_PIN, GPIO.IN)

while True:
    if not (GPIO.input(BATTERY_PIN)):
        os.system(START_RADIO_SERVICE)
        radio.play(LOW_BATTERY_SFX, True)
        os.system(SHUTDOWN_NOW)
        sleep(90)
    sleep(POLL_INTERVAL_IN_SEC)
