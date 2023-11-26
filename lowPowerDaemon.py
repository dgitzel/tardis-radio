from os import system
from time import sleep

import RPi.GPIO as GPIO

from constants import BATTERY_PIN, SHUTDOWN_NOW, START_RADIO_SERVICE, LOW_BATTERY_SFX_PATH, DAEMON_POLL_INTERVAL_IN_SEC
from soxplayer import SoxPlayer

radio = SoxPlayer()
GPIO.setmode(GPIO.BCM)
GPIO.setup(BATTERY_PIN, GPIO.IN)

while True:
    if not (GPIO.input(BATTERY_PIN)):
        system(START_RADIO_SERVICE)
        radio.play(LOW_BATTERY_SFX_PATH, True)
        system(SHUTDOWN_NOW)
        sleep(90)
    sleep(DAEMON_POLL_INTERVAL_IN_SEC)
