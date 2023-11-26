import math
import os.path
import random
from collections import defaultdict, deque
from glob import glob
from time import sleep
from typing import Dict, Deque

from gpiozero import MCP3008

from constants import TUNE_SFX_PATH, MEDIA_ROOT, \
    AUDIO_FILE_TYPE_GLOB, TUNER_POLLING_WINDOW, SONG_SPACING_IN_SEC
from soxplayer import SoxPlayer


class TimeMachine:
    def __init__(self, playlists: Dict[int, Deque]):
        self.radio = SoxPlayer(TUNE_SFX_PATH)
        self.tuner = MCP3008(channel=0)
        self.position: int = self.get_tuner_position()
        self.playlist_by_year: Dict[int, Deque] = playlists
        self.playlist: Deque = self.playlist_by_year.get(self.position)
        self.change_playlist(self.playlist)

    def get_tuner_position(self) -> int:
        """
        Get the average pot from multiple samples.
        """
        num_channels = len(self.playlist_by_year.keys())

        accumulator = 0
        for i in range(TUNER_POLLING_WINDOW):
            accumulator += self.tuner.value
        offset = 0.5 / num_channels
        # Convert (0, 1) to (offset, num_channels + offset), when floored yields (0, num_channels)
        return math.floor(accumulator / TUNER_POLLING_WINDOW * num_channels + offset)

    def change_playlist(self, playlist):
        self.playlist = playlist
        song = self.get_next_song()

        self.radio.stop()
        self.radio.tune_and_play(song, random.uniform(0, 0.5))
        print('[TUNING] ' + str(os.path.basename(song)))

    def get_next_song(self):
        song = self.playlist.pop()
        self.playlist.appendleft(song)
        return song

    def run(self):
        while True:
            # change channel
            position = self.get_tuner_position()
            if position != self.position:  # if the tuner moved, change the playlist and play a new song
                self.position = position
                playlist = self.playlist_by_year.get(position)
                self.change_playlist(playlist)

            if self.radio.is_playing:
                sleep(SONG_SPACING_IN_SEC)
            else:
                self.radio.play(self.get_next_song())


def parse_media_root() -> Dict[int, Deque]:
    ps = defaultdict(deque)  # setup playlists
    for i in glob(os.path.join(MEDIA_ROOT, "[0-9]*")):
        p = deque(glob(os.path.join(i, AUDIO_FILE_TYPE_GLOB)))
        random.shuffle(p)
        ps[int(i)] = p
    return ps


def main():
    ps = parse_media_root()

    # Initialise
    time_machine = TimeMachine(ps)
    # Run the radio
    time_machine.run()
