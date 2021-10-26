from unittest import mock, TestCase
from kloia_exporter.metricService import File
import json


class TestFile(TestCase):

    def test_read_file_and_get_json_body_when_valid_json(self):
        # test valid JSON
        read_data = json.dumps({'a': 1, 'b': 2, 'c': 3})
        mock_open = mock.mock_open(read_data=read_data)
        with mock.patch('builtins.open', mock_open):
            result = File.read_file_and_get_json_body("exporter_data.json")
            self.assertEqual({'a': 1, 'b': 2, 'c': 3}, result)

    def test_read_file_and_get_json_body_when_invalid_json(self):
        # test invalid JSON
        read_data = ''
        mock_open = mock.mock_open(read_data=read_data)
        with mock.patch("builtins.open", mock_open):
            result = File.read_file_and_get_json_body("exporter_data.json")
            self.assertEqual(0, len(result))

    def test_read_file_and_get_json_body_when_file_not_exist(self):
        # test file does not exist
        result = File.read_file_and_get_json_body("exporter_data.json")
        self.assertEqual(0, len(result))
