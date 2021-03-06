from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from flask_migrate import Migrate
from flask import jsonify
import os
import datetime

app = Flask(__name__)
### if runninning locally get postgres uri from env variables
### uri = 'postgresql://user:password@host/db'
db_conn = f"""postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}/{os.environ['DB_NAME']}/"""
print(f"THIS IS {db_conn=}")
app.config['SQLALCHEMY_DATABASE_URI'] = db_conn
db = SQLAlchemy(app)
Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {"schema": "app"}
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(50), unique=True, nullable=False)
    last = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, first, last, email):
        self.first = first
        self.last = last
        self.email = email


class Chat(db.Model):
    __tablename__ = 'chat'
    __table_args__ = {"schema": "app"}
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.TEXT, unique=True, nullable=False)
    sender = db.Column(db.Integer, unique=True, nullable=False)
    reciever = db.Column(db.Integer, unique=True, nullable=False)
    datecreated = db.Column(DateTime(timezone=True),  default=datetime.datetime.now, nullable=True)

    def __init__(self, body, sender, reciever):
        self.body = body
        self.sender = sender
        self.reciever = reciever


class ConversationRow:
    def __init__(self, sender_id, sender_first, sender_last, reciever_id, reciever_first, receiver_last, body, datecreated) -> None:
        self.sender_id = sender_id
        self.sender_first = sender_first
        self.sender_last = sender_last
        self.reciever_id = reciever_id
        self.reciever_first = reciever_first
        self.reciever_last = receiver_last
        self.body = body
        self.datecreated = datecreated

    def to_dict(self):
        return {
            'sender_id': self.sender_id,
            'sender_first': self.sender_first,
        'sender_last': self.sender_last,
        'reciever_id': self.reciever_id,
        'reciever_first': self.reciever_first,
        'reciever_last': self.reciever_last,
        'body': self.body,
        'date': self.datecreated}
        



@app.route('/chat', methods=['POST', 'GET'])
def message():
    if request.method == 'POST':
        body = request.json.get('body')
        sender = int(request.json.get('sender'))
        receiver = int(request.json.get('reciever'))
        chat = Chat(body, sender, receiver)
        db.session.add(chat)
        db.session.commit()

    return jsonify({200: 'OK'}),200

@app.route('/conversation', methods = ['POST', 'GET'])
def conversation():
    if request.method == 'GET':
        participants = request.json.get("participants")
        result = db.engine.execute(f"""
               select u.id, u.first, u.last, ur.id, ur.first, ur.last, body, c.datecreated
                from app.users u
                join app.chat c 
                on u.id = c.sender
                join app.users ur
                on ur.id = reciever
                where 
                (sender = {participants[0]} and reciever = {participants[1]})
                or
                (sender = {participants[1]} and reciever = {participants[0]})
                order by datecreated asc

        """)

        messages = [ ConversationRow(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]) for row in result]
        
        return jsonify([m.to_dict() for m in messages]), 200

@app.route('/user', methods=['POST', 'GET'])
def user():

     if request.method == 'POST':
        first = request.json.get('first')
        last = request.json.get('last')
        email = request.json.get('email')
        user = User(first, last, email)
        db.session.add(user)
        db.session.commit()
        return jsonify({200: 'OK'}),200

