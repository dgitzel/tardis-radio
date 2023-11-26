import math
import os.path
import random
from collections import defaultdict, deque
from glob import glob
from random import choice
from time import sleep
from typing import List

from gpiozero import MCP3008

from constants import DAEMON_POLL_INTERVAL_IN_SEC, TUNE_SFX_PATH, MEDIA_ROOT, \
    AUDIO_FILE_TYPE_GLOB, TUNER_POLLING_WINDOW
from soxplayer import SoxPlayer


class Radio:
    def __init__(self):
        self.radio = SoxPlayer(TUNE_SFX_PATH)
        self.playlist = deque()
        self.tuner = MCP3008(channel=0)
        self.media_by_year = defaultdict(list)

        for i in glob(os.path.join(MEDIA_ROOT, "[0-9]*")):
            key = int(i)
            playlist = glob(os.path.join(i, AUDIO_FILE_TYPE_GLOB))
            random.shuffle(playlist)
            self.media_by_year[key] = playlist

    def get_playlist(self) -> List[str]:
        position = self.get_tuner_position()
        return self.media_by_year.get(position)

    def get_tuner_position(self) -> int:
        num_channels = len(self.media_by_year)

        # get the average pot value after n readings. This reduces channels 'flipping' back and forth
        # when tuned near the borders of two decades.
        accumulator = 0
        for i in range(TUNER_POLLING_WINDOW):
            accumulator += self.tuner.value
        offset = 0.5 / num_channels
        # Convert (0, 1) to (offset, num_channels + offset), when floored yields (0, num_channels)
        position = math.floor(accumulator / TUNER_POLLING_WINDOW * num_channels + offset)
        return position

    def change_playlist(self, playlist):
        self.playlist = playlist
        self.stop()

        # pick the next song
        song = self.playlist.pop()
        # append to the end of the list
        self.playlist.appendleft(song)

        # play the song
        self.tune_and_play(song)
        print('[TUNING] ' + str(song.split("/")[5]))

    def play_next_song(self):
        # pick the next song
        song = self.playlist.pop()
        # append to the end of the list
        self.playlist.appendleft(song)

        # play the song
        self.play(song)

    def run(self):
        while True:
            # change channel when appropriate
            playlist = get_playlist()
            if playlist != CURRENT_CHANNEL_PLAYLIST:
                change_channel(playlist)

            # play next song when appropriate
            if not RADIO.is_playing():
                play_next_song()

            sleep(DAEMON_POLL_INTERVAL_IN_SEC)


if __name__ != "__main__":
    # Initialise
    radio = Radio()
    radio.change_playlist(get_playlist())
    # Run the radio
    radio.run()
