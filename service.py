import sqlite3
import settings
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)
app.config.from_object(settings)


@app.route('/messages/', methods=['POST'])
def create_message():
    """Creates message from request data"""
    json_fields = ['message', 'sender', 'conversation_id']
    req = request.get_json()
    # validate json
    for field in json_fields:
        if field not in req:
            return make_response(jsonify({'error': 'Bad request'}), 400)

    # I have a solution that puts this job into the basic Redis Queue
    # but tests for that was difficult to automate,
    # so here is a solution without a queue
    add_message(req['message'], req['sender'], req['conversation_id'])

    return jsonify("Message added successfully"), 201


@app.route('/conversations/<int:conversation_id>', methods=['GET'])
def get_history_by_id(conversation_id):
    """Returns conversation history for given conversation_id"""
    # request history
    history = get_history(conversation_id)
    # check if history exists
    if not history:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({'id': conversation_id, 'messages': history}), 200


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

