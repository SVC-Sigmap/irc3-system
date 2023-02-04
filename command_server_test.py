import unittest, requests

from command_server import server

class FlaskTest(unittest.TestCase):

    def setUp(self):
        self.server = server.test_client()

    def test_get_status(self):
        self.assertTrue(self.server.get('/api/status').get_json())

    def test_webhook(self):
        response = self.server.post('/webhooks/cmd', json={'SIGMAP-CMD':'Undock'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Undock Executed')
        