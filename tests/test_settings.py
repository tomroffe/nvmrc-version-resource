from os import environ

from unittest import mock, TestCase
from nvmrc_version.settings import Settings


class VersionUnittests(TestCase):
    def test_settings(self):
        settings: Settings = Settings()
        assert isinstance(settings, Settings)

    def test_version_regex_default(self):
        assert Settings().version_regex == r"^v?(?P<major_version>\d+)\.?(?P<minor_version>\d+)?\.?(?P<patch_version>\d+)?"

    def test_filename_default(self):
        assert Settings().filename == ".nvmrc"

    def test_path_blank_default(self):
        assert Settings().path == ""

    @mock.patch.dict(environ, {"NVMRC_PATH": "./test/path"})
    def test_path_string_via_env(self):
        assert Settings().path == "./test/path"

    @mock.patch.dict(environ, {"NVMRC_VERSION_REGEX": r"^.+"})
    def test_regex_string_via_env(self):
        assert Settings().version_regex == r"^.+"

    @mock.patch.dict(environ, {"NVMRC_FILENAME": "test.file"})
    def test_filename_string_via_env(self):
        assert Settings().filename == "test.file"
