import os.path
from os import system
import subprocess
from typing import Optional

from constants import KILL_SOX_PLAYER


class SoxPlayer:
    """
    A wrapper for SoX program. SoX is invoked through shell commands spawned by Python subprocesses
    requirements:
        sudo apt install sox libsox-fmt-all bc
    """

    def __init__(self, sfx_file: Optional[str] = os.path.devnull) -> None:
        self.sox_process = None
        self.sfx_file = sfx_file

    def play(self, song_path: str, blocking: bool = False) -> None:
        """
        PLay a song from a file via SoX.
        """
        self.stop()

        if blocking:
            system(f"AUDIODEV=hw:1,0 /usr/bin/play -q '{song_path}' 2>/dev/null")
        else:
            self.sox_process = subprocess.Popen(['sox', '-V0', '-q', song_path, '-d'])

    def tune_and_play(self, song_path: str, percentage: float = 0.5) -> None:
        """
        Stop the current song, play the tuning sound while fading-in the new song.
        The new song will begin @percentage of the way through (function argument)
        """
        if self.sfx_file is None:
            self.play(song_path)

        # kill old song
        self.stop()

        # find the starting position of the song using the length of the song * percentage.
        # The length is got by soxi and the calculation by bc
        song_starting_position = subprocess.check_output(
            f"echo $(soxi -D \"{song_path}\")*{percentage}/1 | bc",
            shell=True, universal_newlines=True)

        # play the sfx and the new song together
        # fade the new song in allowing time for the tuning to be heard
        cmd1 = subprocess.Popen(
            ['sox', '-V0', '-q', song_path, '-p', 'trim', f'{int(song_starting_position)}', 'fade', '5'],
            stdout=subprocess.PIPE)
        self.sox_process = subprocess.Popen(
            ['sox', '-V0', '-q', '-', '-m', self.sfx_file, '-d'],
            stdin=cmd1.stdout)

    def stop(self):
        """
        Stop all songs currently playing.
        """
        if self.is_playing:
            system(KILL_SOX_PLAYER)

    @property
    def is_playing(self):
        if self.sox_process is None:
            return False
        else:
            return self.sox_process.poll() is None
