from unittest import mock, TestCase
import kloia_exporter.config as config


class TestConfig(TestCase):

    @mock.patch('kloia_exporter.config.get_config_info', return_value={"token": "token"})
    def test_get_info_func(self, mock_get_info_func):
        result = config.get_config_info("database.ini", "postgresql")
        self.assertEqual("token", result["token"])
        mock_get_info_func.assert_called_once()

    @mock.patch('configparser.RawConfigParser.has_section', return_value=True)
    @mock.patch('configparser.RawConfigParser.items', return_value=[("token", "token"), ("path", "path")])
    def test_get_info_func_parser(self, mock_items_func, mock_has_section_func):
        result = config.get_config_info("database.ini", "postgresql")
        self.assertEqual("path", result["path"])
        mock_has_section_func.assert_called_once()
        mock_items_func.assert_called_once()

    @mock.patch('configparser.RawConfigParser.has_section', return_value=False)
    def test_get_info_func_parser_exception(self, mock_has_section_func):
        isThereException = False
        try:
            config.get_config_info("database.ini", "postgresql")
        except Exception:
            isThereException = True

        self.assertEqual(True, isThereException)
        mock_has_section_func.assert_called_once()
