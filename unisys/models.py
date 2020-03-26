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

class MessageHistory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    roomName = db.Column(db.String(100))
    sender = db.Column(db.String(50))
    receiver = db.Column(db.String(50))
    message = db.Column(db.String(800))

    def __repr__(self):
        return f"MessageHistory( roomName:' {self.roomName} ', sender: ' {self.sender} '), receiver: ' {self.receiver} ')"
