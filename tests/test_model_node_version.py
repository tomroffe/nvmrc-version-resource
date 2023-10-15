import unittest

from nvmrc_version.models import NodeVersion


class NodeVersionUnittests(unittest.TestCase):
    def test_node_version_model_setup(self):
        node_version = NodeVersion(major_version=1, minor_version=2, patch_version=3, nvmrc_version="1.2.3")
        assert isinstance(node_version, NodeVersion)

    def test_node_version_full_semver_call(self):
        node_version = NodeVersion(major_version=1, minor_version=2, patch_version=3, nvmrc_version="1.2.3")
        version = node_version.semver
        assert version == "1.2.3"

    def test_node_version_major_minor_semver_call(self):
        node_version = NodeVersion(major_version=1, minor_version=2, nvmrc_version="1.2")
        version = node_version.semver
        assert version == "1.2"

    def test_node_version_major_semver_call(self):
        node_version = NodeVersion(major_version=1, nvmrc_version="1")
        version = node_version.semver
        assert version == "1"
