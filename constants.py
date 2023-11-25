# GPIO Pins
POWER_SWITCH_PIN = 22
KEEP_ALIVE_PIN = 23
BATTERY_PIN: int = 27
# the threshold below can be increased depending on how 'jumpy' your volume pot is
VOLUME_THRESHOLD = 1
POLL_INTERVAL_IN_SEC = 0.05
# Commands
SHUTDOWN_NOW = "sudo shutdown now"
KILL_SOX_PLAYER = "sudo killall -9 sox"
START_RADIO_SERVICE = "sudo systemctl stop tardis-radio.service"
STOP_RADIO_SERVICE = "sudo systemctl stop tardis-radio.service"
# Paths
LOW_BATTERY_SFX = "/home/pi/tardis-radio/media/administrative/lowbattery.mp3"
