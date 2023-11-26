from os import system
from time import sleep

from gpiozero import MCP3008

from constants import VOLUME_THRESHOLD, DAEMON_POLL_INTERVAL_IN_SEC

volume_pot = MCP3008(channel=1)
volume_value = 0

while True:
    # To invert the volume control comment out the other one of the two lines below.
    # newValue = int(volumePot.value) * 255)
    new_value = int((1 - volume_pot.value) * 255)

    has_volume_changed = (new_value < volume_value - VOLUME_THRESHOLD or
                          new_value > volume_value + VOLUME_THRESHOLD)
    if has_volume_changed:
        volume_value = new_value
        system(f'amixer set Master {volume_value}')
    sleep(DAEMON_POLL_INTERVAL_IN_SEC)
