from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from db import db
from models import Message

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


# ----------------------
# Routes
# ----------------------
@app.route("/messages", methods=["GET"])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages])


import logging

@app.route("/messages", methods=["POST"])
def create_message():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        body = data.get("body")
        username = data.get("username")
        if not body or not username:
            return jsonify({"error": "Missing body or username"}), 422
        msg = Message(body=body, username=username)
        db.session.add(msg)
        db.session.commit()
        return jsonify(msg.to_dict()), 201
    except Exception as e:
        logging.error(f"Error creating message: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/messages/<int:id>", methods=["PATCH"])
def update_message(id):
    msg = db.session.get(Message, id)
    if not msg:
        abort(404)
    data = request.get_json()
    msg.body = data.get("body", msg.body)
    db.session.commit()
    return jsonify(msg.to_dict())


@app.route("/messages/<int:id>", methods=["DELETE"])
def delete_message(id):
    msg = db.session.get(Message, id)
    if not msg:
        abort(404)
    db.session.delete(msg)
    db.session.commit()
    return jsonify({}), 204


if __name__ == "__main__":
    app.run(debug=True)
