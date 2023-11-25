import os
from time import sleep

import RPi.GPIO as GPIO

from constants import POWER_SWITCH_PIN, KEEP_ALIVE_PIN, POLL_INTERVAL_IN_SEC, SHUTDOWN_NOW, STOP_RADIO_SERVICE

PLAY_SHUTDOWN_SFX = "play -q /home/pi/tardis-radio/media/administrative/lowbattery.mp3 2>/dev/null"

GPIO.setmode(GPIO.BCM)
GPIO.setup(POWER_SWITCH_PIN, GPIO.IN)
GPIO.setup(KEEP_ALIVE_PIN, GPIO.OUT)

while True:
    GPIO.output(KEEP_ALIVE_PIN, GPIO.HIGH)
    if not GPIO.input(POWER_SWITCH_PIN):
        os.system(STOP_RADIO_SERVICE)
        os.system(PLAY_SHUTDOWN_SFX)
        os.system(SHUTDOWN_NOW)
        sleep(30)
    sleep(POLL_INTERVAL_IN_SEC)
