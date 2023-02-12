import unittest, sys
from unittest.mock import patch
from os.path import abspath, dirname, join
sys.path.insert(0, join(dirname(abspath(__file__)), '..')) # sets the sys directory to the parent so modules can be imported
from irc3_system.signal_scanner import get_signal_data

class TestSignalData(unittest.TestCase):

    def test_get_signal_data(self):
        # Test with expected output
        output = '''
        wlan0     IEEE 802.11  ESSID:"ESSID"
                  Link Quality=70/70  Signal level=-50
                  Bit Rate=144 Mb/s  
                  Access Point: 00:11:22:33:44:55 
                  ESSID:"ESSID"'''
        with unittest.mock.patch('subprocess.run', return_value=unittest.mock.Mock(stdout=output)):
            data = get_signal_data()
            self.assertEqual(data, {
                "link_quality": 100.0,
                "signal_level_dbm": -50,
                "bit_rate": 144,
                "access_point": "00:11:22:33:44:55",
                "essid": "ESSID"
            })

        # Test with unexpected output
        output = '''
        wlan0     IEEE 802.11  ESSID:"ESSID"
                  Link Quality=65/70  Signal level=-50
                  Bit Rate=144 Mb/s
                  Access Point: 00:11:22:33:44:55
                  ESSID:"ESSID"'''
        with unittest.mock.patch('subprocess.run', return_value=unittest.mock.Mock(stdout=output)):
            data = get_signal_data()
            self.assertNotEqual(data, {
                "link_quality": 100.0,
                "signal_level_dbm": -50,
                "bit_rate": 144,
                "access_point": "00:11:22:33:44:55",
                "essid": "ESSID"
            })
