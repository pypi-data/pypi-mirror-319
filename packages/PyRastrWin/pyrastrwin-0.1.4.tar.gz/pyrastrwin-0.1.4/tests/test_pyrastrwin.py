import unittest
from pathlib import Path
from PyRastrWin import RastrWin, DIR_RASTR_WIN_TEST_9

def main():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(__name__)
    runner = unittest.TextTestRunner()
    runner.run(suite)


class RastrWinTest(unittest.TestCase):
    def test_run_rastr_win(self) -> None:
        rastr = RastrWin()
        self.assertEqual(rastr.load(filename=DIR_RASTR_WIN_TEST_9), Path(DIR_RASTR_WIN_TEST_9))
        self.assertTrue(rastr.rgm())
        self.assertEqual(rastr.save(), Path(DIR_RASTR_WIN_TEST_9))
        
        self.assertFalse(rastr.load(filename='DIR_RASTR_WIN_TEST_9'), Path(DIR_RASTR_WIN_TEST_9))


if __name__ == '__main__':
    main()