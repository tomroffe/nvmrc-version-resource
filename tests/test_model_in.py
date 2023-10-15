import io
import re
import pytest
import unittest
from testfixtures import OutputCapture

from unittest.mock import patch, mock_open

from nvmrc_version.input import in_, check_destination_path, load_request_payload, get_nvmrc_regex, get_nvmrc_version, main
from nvmrc_version.models import InPayload


class InFunctionUnittests(unittest.TestCase):
    def test_check_destination_path(self):
        path = check_destination_path("./")
        self.assertEqual(path, "./")

    def test_check_destination_path_raises_error(self):
        with pytest.raises(SystemExit) as execinfo:
            _ = check_destination_path("http://")
        self.assertEqual(execinfo.type, SystemExit)
        self.assertEqual(execinfo.value.code, 1)

    def test_load_request_payload(self):
        input_json = '{"source": {}, "version": {"ref": "1.2.3"}}'
        with patch("sys.stdin", io.StringIO(input_json)):
            payload = load_request_payload()
        self.assertIsInstance(payload, InPayload)

    def test_load_request_payload_raises_error(self):
        with patch("sys.stdin", io.StringIO("{}")):
            with pytest.raises(SystemExit) as execinfo:
                _ = load_request_payload()
            self.assertEqual(execinfo.type, SystemExit)
            self.assertEqual(execinfo.value.code, 1)

    def test_get_nvmrc_regex_with_blank_source(self):
        input_json = '{"source": {}, "version": {"ref": "1.2.3"}}'
        with patch("sys.stdin", io.StringIO(input_json)):
            payload = load_request_payload()
            regex = get_nvmrc_regex(payload)
        self.assertIsInstance(regex, re.Pattern)

    def test_get_nvmrc_regex_without_source(self):
        input_json = '{"version": {"ref": "1.2.3"}}'
        with patch("sys.stdin", io.StringIO(input_json)):
            payload = load_request_payload()
            regex = get_nvmrc_regex(payload)
        self.assertIsInstance(regex, re.Pattern)

    def test_get_nvmrc_regex_with_source_regex(self):
        input_json = '{"source": {"regex": "^.+"}, "version": {"ref": "1.2.3"}}'
        with patch("sys.stdin", io.StringIO(input_json)):
            payload = load_request_payload()
            regex = get_nvmrc_regex(payload)
        self.assertIsInstance(regex, re.Pattern)

    def test_get_nvmrc_version(self):
        input_json = '{"source": {}, "version": {"ref": "1.2.3"}}'
        with patch("sys.stdin", io.StringIO(input_json)):
            payload = load_request_payload()
            with patch("builtins.open", mock_open(read_data="1.2.3")) as open:
                version = get_nvmrc_version("", payload)
                self.assertEqual(version, "1.2.3")
                open.assert_called_with("/.nvmrc", "r", encoding="utf8")

    def test_in_function(self):
        input_json = '{"source": {}, "version": {"ref": "1.2.3"}}'
        with patch("sys.stdin", io.StringIO(input_json)):
            payload = load_request_payload()
            with patch("builtins.open", mock_open(read_data="1.2.3")):
                with OutputCapture(separate=True) as output:
                    in_("", payload)
        out = output.stdout.getvalue()
        print(out)
        self.assertTrue('"version"' in out)
        self.assertTrue('"ref": "1.2.3"' in out)
        self.assertTrue('"metadata"' in out)

    def test_in_function_no_regex_match(self):
        input_json = '{"source": {"regex": "^This should not match"}, "version": {"ref": "1.2.3"}}'
        with patch("sys.stdin", io.StringIO(input_json)):
            payload = load_request_payload()
            with patch("builtins.open", mock_open(read_data="1.2.3")):
                with pytest.raises(SystemExit) as execinfo:
                    in_("", payload)

        self.assertEqual(execinfo.type, SystemExit)
        self.assertEqual(execinfo.value.code, 1)

    def test_main_function(self):
        input_json = '{"source": {}, "version": {"ref": "1.2.3"}}'
        testargs = [None, "tests/"]

        with patch("sys.argv", testargs):
            with patch("sys.stdin", io.StringIO(input_json)):
                with patch("builtins.open", mock_open(read_data="1.2.3")):
                    main()
