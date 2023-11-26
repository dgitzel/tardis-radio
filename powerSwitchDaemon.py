from os import system
from time import sleep

import RPi.GPIO as GPIO

from constants import POWER_SWITCH_PIN, KEEP_ALIVE_PIN, DAEMON_POLL_INTERVAL_IN_SEC, SHUTDOWN_NOW, STOP_RADIO_SERVICE, \
    SHUTDOWN_SFX_PATH
from soxplayer import SoxPlayer

radio = SoxPlayer()
GPIO.setmode(GPIO.BCM)
GPIO.setup(POWER_SWITCH_PIN, GPIO.IN)
GPIO.setup(KEEP_ALIVE_PIN, GPIO.OUT)

while True:
    GPIO.output(KEEP_ALIVE_PIN, GPIO.HIGH)
    if not GPIO.input(POWER_SWITCH_PIN):
        system(STOP_RADIO_SERVICE)
        radio.play(SHUTDOWN_SFX_PATH, True)
        system(SHUTDOWN_NOW)
        sleep(30)
    sleep(DAEMON_POLL_INTERVAL_IN_SEC)
