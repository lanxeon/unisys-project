from unisys import db, bcrypt
from unisys.models import User, Message_room, Message

db.drop_all()
db.create_all()

user1 = User(fname = "Swapnonil", lname = "Bandyopadhay", usn = "lanxion", 
email = "swapdasa@gmail.com", pwd = bcrypt.generate_password_hash("theandre2131").decode('utf-8'))

user2 = User(fname = "Sonali", lname = "Pandey", usn = "sonali42", 
email = "sonali.pandey@gmail.com", pwd = bcrypt.generate_password_hash("sonali123").decode('utf-8'))

db.session.add(user1)
db.session.add(user2)

db.session.commit()