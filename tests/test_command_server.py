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
        
    def test_get_signal(self):
        response = self.server.get('/api/status')
        self.assertEqual(response.status_code, 200)

    def test_webhook(self):
        # Test for POST with Teleop_Keyboard command
        response = self.server.post('/webhooks/cmd', json={'SIGMAP-CMD':'Teleop_Keyboard'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Teleop_Keyboard Action Executed')
        
        # Test for POST with Teleop_Joystick command
        response = self.server.post('/webhooks/cmd', json={'SIGMAP-CMD':'Teleoperation_Joystick'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Teleop_Joystick Action Executed')
        
        # Test for POST with StopAll command
        response = self.server.post('/webhooks/cmd', json={'SIGMAP-CMD':'StopAll'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'All processes terminated')
        
        # Test for POST with unknown command
        response = self.server.post('/webhooks/cmd', json={'SIGMAP-CMD':'Invalid'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Unknown Command')
        
        # Test for POST with no command
        response = self.server.post('/webhooks/cmd', json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Webhook received without command!')
