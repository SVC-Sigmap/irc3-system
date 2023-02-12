import unittest, sys
from os.path import abspath, dirname, join
sys.path.insert(0, join(dirname(abspath(__file__)), '..')) # sets the sys directory to the parent so modules can be imported
from irc3_system.command_server import server
from irc3_system.data_collection import robot_status

class TestServer(unittest.TestCase):

    def setUp(self):
        self.server = server.test_client()

    def test_get_status(self):
        response = self.server.get('/api/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, robot_status)

    def test_webhook(self):
        # Test for POST with Undock command
        response = self.server.post('/webhooks/cmd', json={'SIGMAP-CMD':'Undock'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Undock Executed')
        
        # Test for POST with unknown command
        response = self.server.post('/webhooks/cmd', json={'SIGMAP-CMD':'Invalid'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Unknown Command')
        
        # Test for POST with no command
        response = self.server.post('/webhooks/cmd', json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Webhook received without command!')
