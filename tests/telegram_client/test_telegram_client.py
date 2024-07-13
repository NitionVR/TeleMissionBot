import configparser
import unittest
from client.telegram_client import config_file

class TestTelegramClient(unittest.TestCase):
    
    #Test that the config file is read as expected by ConfigParser
    def test_config_file(self):
        config = config_file()
        self.assertIsInstance(config, configparser.ConfigParser)
        self.assertEqual(config.section(), ['Telegram'])

if __name__  == "__main__":
    unittest.main()
