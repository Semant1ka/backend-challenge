import sqlite3
import settings
import re
from schema import *
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)
app.config.from_object(settings)


@app.route('/messages/', methods=['POST'])
def create_message():
    """Creates message from request data"""
    req = request.get_json()
    # validate json
    errors = MessageSchema().validate(req)
    if len(errors) > 0:
        return make_response(jsonify({'error': 'Bad request ', 'error_message': errors}), 400)

    add_message(req['message'], req['sender'], req['conversation_id'])

    return jsonify("Message added successfully"), 201


@app.route('/conversations/<conversation_id>', methods=['GET'])
def get_history_by_id(conversation_id):
    """Returns conversation history for given conversation_id"""
    # validate id
    is_number = re.match(re.compile("^[0-9]+$"), conversation_id)
    if not is_number:
        return make_response(jsonify({'error': 'Bad Request'}), 400)
    # request history
    history = get_history(conversation_id)
    # check if history exists
    if not history:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({'id': int(conversation_id), 'messages': history}), 200


def get_history(conversation_id):
    """Retrieves history form Db"""
    with sqlite3.connect(app.config['DATABASE']) as conn:
        c = conn.cursor()
        q = "SELECT * FROM messages WHERE conversation_id=? ORDER BY dt DESC"
        rows = c.execute(q, (int(conversation_id),))

        return [{'sender': r[3], 'message': r[2], 'created': r[1]} for r in rows]


def add_message(message, sender, conversation_id):
    """Pushes message into Db"""
    with sqlite3.connect(app.config['DATABASE']) as conn:
        c = conn.cursor()
        q = "INSERT INTO messages VALUES (NULL, datetime('now'),?,?,?)"
        c.execute(q, (message, sender, conversation_id))
        conn.commit()
