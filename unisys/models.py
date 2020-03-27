from datetime import datetime
from unisys import db, lm
from flask_login import UserMixin

@lm.user_loader
def load_user(uid):
	return User.query.get(int(uid))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    usn = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    pwd = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User(name:'{self.fname} {self.lname}', email:'{self.email}', usn: '{self.usn}')"

class Message_room(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    roomName = db.Column(db.String(100), unique = True)
    user1 = db.Column(db.String(50), nullable = False)
    user2 = db.Column(db.String(50), nullable = False)
    messages = db.relationship("Message", backref = "room", lazy = True)

    def __repr__(self):
        return f"Message_room( roomName:'{self.roomName}' )"

class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sender = db.Column(db.String(50), nullable = False)
    receiver = db.Column(db.String(50), nullable = False)
    message = db.Column(db.Text, nullable = False)
    room_id = db.Column(db.Integer, db.ForeignKey('message_room.id'), nullable=False)

    def __repr__(self):
        return f"Messages( sender: '{self.sender}'), receiver: '{self.receiver}' )"

