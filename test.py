import os.path
import unittest
from collections import defaultdict, deque

from soxplayer import SoxPlayer
from timemachine import TimeMachine, parse_media_root


# Tests for the daemons and radio

class TestTimeMachine(unittest.TestCase):

    def setUp(self):
        ps = defaultdict(deque)
        self.tm = TimeMachine(ps)

    def test_parse_media_root(self):
        ps = parse_media_root()
        self.assertDictEqual(ps, defaultdict(deque))


class TestSoxPlayer(unittest.TestCase):
    def setUp(self):
        self.sp = SoxPlayer()

    def test_init(self):
        self.assertIsNone(self.sp.sox_process)
        self.assertEquals(self.sp.sfx_file, os.path.devnull)
        self.assertFalse(self.sp.is_playing)

    def test_play_and_stop(self):
        # a play test requires an RPi and functioning output pin
        # self.sp.play(os.path.devnull)
        self.sp.stop()


if __name__ == "__main__":
    unittest.main()
