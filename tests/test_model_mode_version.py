import unittest

from nvmrc_version.models import NodeVersion
from nvmrc_version.settings import Settings


class NodeVersionUnittests(unittest.TestCase):
    def test_node_version_model_setup(self):
        test_data = {"major_version": 1, "minor_version": 2, "patch_version": 3, "nvmrc_version": "1.2.3"}
        node_version = NodeVersion(**test_data)
        assert isinstance(node_version, NodeVersion)

    def test_node_version_semver_call(self):
        test_data = {"major_version": 1, "minor_version": 2, "patch_version": 3, "nvmrc_version": "1.2.3"}
        node_version = NodeVersion(**test_data)
        version = node_version.semver
        assert version == "1.2.3"
