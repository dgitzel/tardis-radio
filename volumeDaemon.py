import os
import time

from gpiozero import MCP3008

from constants import VOLUME_THRESHOLD, POLL_INTERVAL_IN_SEC

volumePot = MCP3008(channel=1)
volumeValue = 0

while True:
    # To invert the volume control comment out the other one of the two lines below.
    # newValue = int(volumePot.value) * 255)
    newValue = int((1 - volumePot.value) * 255)

    has_volume_changed = (newValue < volumeValue - VOLUME_THRESHOLD or
                          newValue > volumeValue + VOLUME_THRESHOLD)
    if has_volume_changed:
        volumeValue = newValue
        os.system(f'amixer set Master {volumeValue}')
    time.sleep(POLL_INTERVAL_IN_SEC)
