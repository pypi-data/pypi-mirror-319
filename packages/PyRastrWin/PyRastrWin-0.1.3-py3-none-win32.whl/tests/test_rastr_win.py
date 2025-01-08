import unittest
from pathlib import Path

from PyRastrWin import RastrWin, DIR_RASTR_WIN_TEST_9


class RastrWinTest(unittest.TestCase):
    def test_run_rastr_win(self) -> None:
        rastr = RastrWin()
        self.assertEqual(rastr.load(filename=DIR_RASTR_WIN_TEST_9), Path(DIR_RASTR_WIN_TEST_9))
        self.assertTrue(rastr.rgm())
        self.assertEqual(rastr.save(), Path(DIR_RASTR_WIN_TEST_9))