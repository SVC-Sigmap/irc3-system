#!/usr/bin/env python3
import unittest, sys
from time import sleep
from os.path import abspath, dirname, join
from unittest.mock import patch
sys.path.insert(0, join(dirname(abspath(__file__)), '..')) # sets the sys directory to the parent so modules can be imported
from irc3_system.command_server import server
from irc3_system.robot_status import robot_status

header_missing_json = {'error': 'authorization header missing'}
header_invalid_token = {'error': 'invalid token'}

class TestServer(unittest.TestCase):

    # Starts a Flask test client using the Sigmap 'server' implementation from irc3_system.command_server module
    def setUp(self):
        self.server = server.test_client()
        
#### Status Endpoint Tests #####
    # Basis Path:
    # Tests a request with a vlid authentication header to
    # the /api/status endpoint. Asserts matching JSON reponse and
    # asserts status code 200.
    @patch('firebase_admin.auth.verify_id_token')
    def test_get_status(self, mock_verify_id_token):
        mock_verify_id_token.return_value = {'user': 'user123'}
        headers = {'Authorization': 'valid_token'}
        response = self.server.get('/api/status', headers=headers)
        self.assertEqual(response.status_code, 200)
        # robot_status will appends Firebase current user
        self.assertEqual(response.json, robot_status)
        
    # Basis Path:
    # Tests a request with a mising authentication header to
    # the /api/status endpoint. Asserts matching error JSON and
    # asserts status code 401.
    def test_get_status_missing_token(self):
        headers = {}
        response = self.server.get('/api/status', headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, header_missing_json)
        
    # Basis Path:
    # Tests a request to the /api/status endpoint that contains
    # an authenticatoin header that will not validate with firebase.
    # Should return apprporiate JSON that indicates an invalid token
    # was sent to the server.
    @patch('firebase_admin.auth.verify_id_token')
    def test_get_status_invalid_token(self, mock_verify_id_token):
        mock_verify_id_token.side_effect = ValueError("Invalid token")
        headers = {'Authorization': 'invalid_token'}
        response = self.server.get('/api/status', headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, header_invalid_token)

#### Signal Endpoint Tests #####
    # Basis Path:
    # Tests a request sent to the /api/signal endpoint that
    # contains a valid authorization header. Should return the proper
    # JSON that has signal data. This signal data however always changes
    # so we assert the returned status code is 200
    @patch('firebase_admin.auth.verify_id_token')
    def test_get_signal(self, mock_verify_id_token):
        mock_verify_id_token.return_value = {'user': 'user123'}
        headers = {'Authorization': 'valid_token'}
        response = self.server.get('/api/signal', headers=headers)
        self.assertEqual(response.status_code, 200)
        
    # Basis Path:
    # Test a request sent to the /api/signal enpoint that does not
    # contain an authorization token. 
    # Asserts that the json response is equal to
    # the invalid token json response. Also asserts that status 401 was returned.
    def test_get_signal_missing_token(self):
        headers = {}
        response = self.server.get('/api/signal', headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, header_missing_json)
        
    # Basis Path:
    # Test a request to the /api/signal endpoint with an invalid 
    # authorization header. Asserts the JSON response is equal to the 
    # invalid token response. Also asserts status code 401.
    @patch('firebase_admin.auth.verify_id_token')
    def test_get_signal_invalid_token(self, mock_verify_id_token):
        mock_verify_id_token.side_effect = ValueError("Invalid token")
        headers = {'Authorization': 'invalid_token'}
        response = self.server.get('/api/signal', headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, header_invalid_token)

#### Webhook Tests ####
    # Basis Path:
    # Test a POST request to the /webhooks/cmd endpoint. This POST is sent with an invalid token
    # and asserts that the JSON response is equal to the invalid token 
    # expected JSON response. Also asserts status code 401.
    @patch('firebase_admin.auth.verify_id_token')
    def test_webhook_cmd_invalid_token(self, mock_verify_id_token):
        mock_verify_id_token.side_effect = ValueError("Invalid token")
        headers = {'Authorization': 'invalid_token'}
        response = self.server.post('/webhooks/cmd', headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, header_invalid_token)
        
    # Basis Path:
    # Test a POST request to /webhooks/cmd endpoint containing no authorization
    # headers. This test will assert that the json response is the json missing
    # header response. It will also assert status code 401.
    def test_webhook_cmd_missing_token(self):
        headers = {}
        response = self.server.post('/webhooks/cmd', headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, header_missing_json)

    # Basis Path:
    # Test a POST request to /webhooks/cmd endpoint containing a valid
    # authorization token. This test will send the Undock command to the server.
    # Asserts that the undock command was executed, as well as status code 200.
    @patch('firebase_admin.auth.verify_id_token')
    def test_webhook_cmd_undock(self, mock_verify_id_token):
        mock_verify_id_token.return_value = {'user': 'user123'}
        headers = {'Authorization': 'valid_token'}
        # Test for POST with Undock command
        response = self.server.post('/webhooks/cmd', json={'SIGMAP-CMD':'Undock'}, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Undock Executed')

    # Basis Path:
    # Test a POST request to /webhooks/cmd endpoint containing a valid
    # authorization token. This test will send the Hallway Travel
    # choreography command to the server.
    # Asserts that the undock command was executed, as well as status code 200.
    @patch('firebase_admin.auth.verify_id_token')
    def test_webhook_cmd_undock(self, mock_verify_id_token):
        mock_verify_id_token.return_value = {'user': 'user123'}
        headers = {'Authorization': 'valid_token'}
        # Test for POST with Undock command
        response = self.server.post('/webhooks/cmd', json={'SIGMAP-CMD':'HallwayTravel'}, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hallway travel complete')
        
    # Basis Path:
    # Test a POST request to the /webooks/cmd endpoint containing a valid authorization header.
    # This post request contains the StopAll command for the server.
    # Assert that all processes have been terminated, as well as status
    # code 200
    @patch('firebase_admin.auth.verify_id_token')
    def test_webhook_cmd_stopall(self, mock_verify_id_token):
        sleep(2) # Sleep 2 second(s) to wait for the previous process start
        mock_verify_id_token.return_value = {'user': 'user123'}
        headers = {'Authorization': 'valid_token'}
        response = self.server.post('/webhooks/cmd', json={'SIGMAP-CMD':'StopAll'}, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'All processes terminated')
        
    # Basis Path:
    # Test a POST request to /webhooks/cmd containing a valid authorization header.
    # This post request will contain an invalid SIGMAP-CMD json value.
    # Assert that the server returns 'Unknown Command' and that the status code is 200.
    @patch('firebase_admin.auth.verify_id_token')
    def test_webhook_cmd_invalid(self, mock_verify_id_token):
        mock_verify_id_token.return_value = {'user': 'user123'}
        headers = {'Authorization': 'valid_token'}
        # Test for POST with unknown command
        response = self.server.post('/webhooks/cmd', json={'SIGMAP-CMD':'Invalid'}, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Unknown Command')
        
    # Basis Path:
    # Test a POST request to the /webhooks/cmd endpoint. with a valid authorization header.
    # This request does not contain any robot commands. Asserts that the server returns no command found
    # and status code 200.
    @patch('firebase_admin.auth.verify_id_token')
    def test_webhook_cmd_no_json(self, mock_verify_id_token):
        mock_verify_id_token.return_value = {'user': 'user123'}
        headers = {'Authorization': 'valid_token'}
        # Test for POST with no command
        response = self.server.post('/webhooks/cmd', json={}, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Webhook received without command!')

if __name__ == '__main__':
    unittest.main()
