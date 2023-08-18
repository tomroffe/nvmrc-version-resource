import unittest

from nvmrc_version.models import Source
from nvmrc_version.settings import Settings


class SourceUnittests(unittest.TestCase):
    def test_source_model_setup(self):
        regex = Settings().version_regex
        path = Settings().path
        filename = Settings().filename
        test_data = {"regex": regex, "path": path, "filename": filename}
        source = Source(**test_data)
        assert isinstance(source, Source)
