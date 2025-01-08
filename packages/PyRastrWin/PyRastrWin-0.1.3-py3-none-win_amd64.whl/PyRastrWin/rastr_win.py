# Python stdlib imports
import logging
from pathlib import Path

# Local imports
from .logging_config.loggers import configure_logging_save_file
from .file_io import load, save, DIR_RASTR_WIN_TEST_9
from .calculations import rgm, run, run_ems
from .settings import settings_for_alt_unit, settings_for_dynamic, settings_for_mdn, settings_for_equivalent, settings_for_regim


# import pywin32
from win32com.client import Dispatch

configure_logging_save_file(level=logging.DEBUG)

class RastrWin:
    def __init__(self):
        self.RASTR = Dispatch("Astra.Rastr")
        self.filename = None
    
    def __str__(self):
        return self.RASTR

    def load(self, filename: Path) -> Path:
        self.filename = filename
        return load(rastr_win=self.RASTR, filename=filename)

    def save(self) -> Path:
        return save(rastr_win=self.RASTR, filename=self.filename)

    def rgm(self) -> bool:
        return rgm(rastr_win=self.RASTR)


