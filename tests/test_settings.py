import os

from unittest import mock, TestCase
from nvmrc_version.settings import Settings


class VersionUnittests(TestCase):
    def test_settings(self):
        settings: Settings = Settings()
        assert isinstance(settings, Settings)

    def test_path_blank_default(self):
        s = Settings()
        assert s.path == ""

    @mock.patch.dict(os.environ, {"NMVRC_PAHT": "testing"})
    def test_path_string_via_env(self):
        path = Settings().path
        assert path == "testing"
