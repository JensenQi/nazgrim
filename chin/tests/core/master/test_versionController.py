import os
import time

os.chdir('../../../')

from unittest import TestCase
from core.master.VersionController import VersionController


class TestVersionController(TestCase):
    def setUp(self):
        self.version_controller = VersionController()

    def test_serve(self):
        self.version_controller.serve('start')
        time.sleep(10)
        self.version_controller.serve('stop')
        self.version_controller.serve('start')
