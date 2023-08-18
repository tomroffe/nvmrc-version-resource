import unittest

from nvmrc_version.models import Version


class VersionUnittests(unittest.TestCase):
    def test_version_model_setup(self):
        test_data = {"ref": "1.2.3"}
        version = Version(**test_data)
        assert isinstance(version, Version)
