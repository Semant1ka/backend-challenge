import json
import os
import sqlite3
import tempfile
import unittest
import service
import settings
import tests.data as data


class BaseFixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        service.app.config.from_object(settings)
        cls.db_fd, service.app.config['DATABASE'] = tempfile.mkstemp()
        service.app.config['TESTING'] = True
        cls.app = service.app.test_client()

        with sqlite3.connect(service.app.config['DATABASE']) as conn:
            sql_path = os.path.join(service.app.config['APP_ROOT'], 'db_init.sql')
            with open(sql_path, 'r') as f:
                cmd = f.read()
                c = conn.cursor()
                c.execute(cmd)
                conn.commit()

    @classmethod
    def tearDownClass(cls):
        os.close(cls.db_fd)
        os.unlink(service.app.config['DATABASE'])


class TestApi(BaseFixture):

    def test_create_message_succeed(self):
        # check status code
        self.assertEqual(self.create_message(data.test_messages['anson_valid']), 201)

        # check record actually added to Db
        self.assertEqual(len(self.check_message_in_db(data.test_messages['anson_valid']).fetchall()), 1)

    def test_create_message_bad_request(self):
        # check status code
        self.assertEqual(self.create_message(data.test_messages['anson_invalid']), 400)

    def test_get_history_succeed(self):
        # should we check date, how?
        expected_response = {

                "id": 1111,
                "messages": [
                    {
                        "sender": "bohemian",
                        "message": "Is this the real life? Is this just fantasy?"
                    },
                    {
                        "sender": "rhapsody",
                        "message": "Caught in a landslide, no escape from reality"
                    }
                ]
            }

        if self.create_message(data.test_messages['bohemian_valid']) is not 201 \
                or self.create_message(data.test_messages['rhapsody_valid']) is not 201:
            raise Exception("Failed to submit new messages")

        # request history
        response = self.app.get("/conversations/1111")

        # check status code
        self.assertEqual(response.status_code, 200)

        # check response data
        actual_response = json.loads(response.get_data(as_text=True))

        # there should be a better solution to compare json objects,
        self.assertEqual(actual_response['id'], expected_response['id'])

        # workaround so we not checking message create date yet
        for element in actual_response['messages']:
                element.pop('created', None)

        pairs = zip(actual_response['messages'], expected_response['messages'])

        # check all data is correct
        self.assertFalse(any(x != y for x, y in pairs))

    def test_get_history_not_found(self):
        # request history
        response = self.app.get("/conversations/0000")

        # check status code
        self.assertEqual(response.status_code, 404)

    def test_bad_conversation_id(self):
        # request history
        response = self.app.get("/conversations/test")

        # check status code
        self.assertEqual(response.status_code, 400)

    def create_message(self, message):
        """Helper method to add a message"""
        message = json.dumps(message)
        response = self.app.post("/messages/", data=message, content_type='application/json')
        return response.status_code

    def check_message_in_db(self, message):
        """Helper method to check data in Db"""
        with sqlite3.connect(service.app.config['DATABASE']) as conn:
            c = conn.cursor()
            q = "SELECT * FROM messages WHERE conversation_id=? AND sender=? AND message=? ORDER BY dt DESC"
            c.execute(q, (int(message['conversation_id']),
                          message['sender'],
                          message['message']))
            return c




