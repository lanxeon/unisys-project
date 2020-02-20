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