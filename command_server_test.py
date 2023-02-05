import unittest
import data_collection

from command_server import server

class TestServer(unittest.TestCase):

    def setUp(self):
        self.server = server.test_client()

    def test_get_status(self):
        response = self.server.get('/api/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, data_collection.robot_status)

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