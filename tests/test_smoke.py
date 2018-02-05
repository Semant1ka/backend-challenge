import unittest
import requests
import json
import tests.data as data
import subprocess
import os
import time

"""
Don't run this tests from docker or if you don't have python3 link, or fix subrpocess command.
Maybe build another docker for this?

Looks like a lot of duplication here from unit tests. How to tackle that?
"""


class SmokeTests(unittest.TestCase):
    process_id = ""
    
    @classmethod
    def setUpClass(cls):

        cls.process_id = subprocess.Popen(["python3", cls.this_dir().replace("tests", "app.py")])
        # wait till Flask wake up
        time.sleep(5)
        cls.post_message = "/messages/"

        # should we use test db or use app's db? how will we clean up db after tests if it is not test db?
        # should we add an API function which allow us to delete messages?

    @classmethod
    def tearDownClass(cls):
        cls.process_id.kill()

    def test_smoke_create_message_succeed(self):
        # check status code
        self.assertEqual(self.send_message(data.test_messages['anson_valid']), 201)

    def test_smoke_create_message_failed(self):
        # check invalid field name
        self.assertEqual(self.send_message( data.test_messages['anson_invalid']), 400,
                         "Check invalid json field name")

        # check invalid conversation_id value
        self.assertEqual(self.send_message(data.test_messages['anson_invalid_id']), 400,
                         "Check invalid json field format: conversation id is string")

    def test_smoke_get_history_failed(self):

        # check non-existing conversation id
        self.assertEqual(self.get_history("/conversations/0000"), 404)

        # check invalid conversation id
        self.assertEqual(self.get_history("/conversations/foobar"), 400)

    def test_smoke_get_history_succeed(self):
        r_code = self.send_message(data.test_messages['anson_valid'])
        if r_code is not 201:
            raise Exception("Failed to send message")

        self.assertEqual(self.get_history("/conversations/{}".
                                          format(data.test_messages['anson_valid']['conversation_id'])), 200)
        # TODO: also check json body here


    def send_message(self, message):
        json_message = json.dumps(message)
        r = requests.post('http://0.0.0.0:5000{}'.format(self.post_message),
                          data=json_message, headers={'content-type': 'application/json'})
        return r.status_code

    def get_history(self, address):
        r = requests.get('http://0.0.0.0:5000{}'.format(address))
        return r.status_code

    @staticmethod
    def this_dir():
        return os.path.dirname(os.path.realpath(__file__))
