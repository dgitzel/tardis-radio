from os import path
# GPIO Pins
POWER_SWITCH_PIN = 22
KEEP_ALIVE_PIN = 23
BATTERY_PIN: int = 27
# Parameters
# the threshold below can be increased depending on how 'jumpy' your volume pot is
TUNER_POLLING_WINDOW = 20
VOLUME_THRESHOLD = 1
DAEMON_POLL_INTERVAL_IN_SEC = 0.05
SONG_SPACING_IN_SEC = 0.25
AUDIO_FILE_TYPE_GLOB = "*.{mp3}"
# Commands
SHUTDOWN_NOW = "sudo shutdown now"
KILL_SOX_PLAYER = "sudo killall -9 sox"
START_RADIO_SERVICE = "sudo systemctl stop tardis-radio.service"
STOP_RADIO_SERVICE = "sudo systemctl stop tardis-radio.service"
# Paths
INSTALL_ROOT = "/home/pi/tardis-radio"
MEDIA_ROOT = path.join(INSTALL_ROOT, "media")
SFX_ROOT = path.join(MEDIA_ROOT, "sfx")
LOW_BATTERY_SFX_PATH = path.join(SFX_ROOT, "low-battery.mp3")
SHUTDOWN_SFX_PATH = path.join(SFX_ROOT, "shutdown.mp3")
TUNE_SFX_PATH = path.join(SFX_ROOT, "static.mp3")
