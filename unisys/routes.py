from flask import render_template, url_for, request, redirect, flash, request, session, Response
from unisys import app, lm, bcrypt, db, socketio
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import send, emit, join_room, leave_room
import os
import unisys.Object_detection_webcam as objDetApi
from unisys.forms import Registration, Login, Chat
from unisys.models import User, MessageHistory
from PIL import Image
from gtts import gTTS
from sqlalchemy import or_
#from pygame import mixer

users = {}
#rooms = []
i = 0

@app.route('/')
@app.route('/home')
def home():
	full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'unisys_logo.jpg')
	full_filename1 = os.path.join(app.config['UPLOAD_FOLDER'], 'blue.jfif')
	full_filename2 = os.path.join(app.config['UPLOAD_FOLDER'], 'slide3.jpg')
	full_filename3 = os.path.join(app.config['UPLOAD_FOLDER'], 'orange.jfif')
	full_filename4 = os.path.join(app.config['UPLOAD_FOLDER'], 'sonali.png')
	full_filename5 = os.path.join(app.config['UPLOAD_FOLDER'], 'tp-01-02.jpeg')
	full_filename6 = os.path.join(app.config['UPLOAD_FOLDER'], 'slide4.jpg')
	full_filename7 = os.path.join(app.config['UPLOAD_FOLDER'], 'slide5.jfif')
	full_filename8 = os.path.join(app.config['UPLOAD_FOLDER'], 'swapnonil.png')
	full_filename9 = os.path.join(app.config['UPLOAD_FOLDER'], 'sushmitha.png')
	full_filename10 = os.path.join(app.config['UPLOAD_FOLDER'], 'zeme.png')
	return render_template('home.html',user_image = full_filename,user_image1 = full_filename1,user_image2 = full_filename2,user_image3 = full_filename3,user_image4 = full_filename4,bg_image = full_filename5,
		user_image6 = full_filename6,user_image7 = full_filename7,user_image8 = full_filename8,user_image9 = full_filename9,user_image10 = full_filename10)

'''
@app.route('/about')
def about():
    return '<h1>About Page</h1>' 
'''

@app.route('/register', methods = ['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = Registration()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.pwd.data).decode('utf-8')
		user = User(fname = form.fname.data, lname = form.lname.data, usn = form.usn.data, pwd = hashed_password, email = form.email.data)
		db.session.add(user)
		db.session.commit()
		flash(f'Registered successfully, You can now Login with your account', 'success')
		return redirect(url_for('login'))

	return render_template('register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	full_filename11 = os.path.join(app.config['UPLOAD_FOLDER'], 'login.jpeg')
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = Login()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user and bcrypt.check_password_hash(user.pwd , form.pwd.data):
			login_user(user, remember=form.remember.data)
			flash(f'Logged in successfully', 'success')
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))

	return render_template('login.html', form = form,user_image = full_filename11)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route('/chat', methods = ['GET', 'POST'])
@login_required
def chat():
	form = Chat()
	user_connected = False
	if form.validate_on_submit():
		print("hey, form validated")
		sender = current_user.usn
		receiver = form.receiver.data
		messages = MessageHistory.query.filter(or_( MessageHistory.roomName == sender+"&&&"+receiver, MessageHistory.roomName == receiver+"&&&"+sender)).all()
		user_connected = True
		return render_template('chat.html', receiver = receiver, user_connected = user_connected, messages = messages)
	return render_template('chat.html', form = form, user_connected = user_connected)


@app.route('/account')
@login_required
def account():
	return render_template('account.html')


@app.route('/image', methods=['POST'])
def image():
	try:
		#acquire image from XHR
		image_file = request.files['image']
		#get ticked value of autoCorrect Checkbox
		autoCorrect = request.form.get('autoCorrect')

		# Set an image confidence threshold value to limit returned data
		threshold = request.form.get('threshold')
		if threshold is None:
			threshold = 0.90
		else:
			threshold = float(threshold)
			
		# finally run the image through tensor flow object detection`
		image_object = Image.open(image_file)
		objects = objDetApi.get_objects(image_object, autoCorrect)
		return objects

	except Exception as e:
		print('POST /image error: '+ str(e))
		return e


@app.route('/tts', methods = ['POST'])
def tts():
	global i
	message = request.form.get('recMsg')
	language = 'en'
	i+=1
	myobj = gTTS(text=message, lang=language, slow=False)
	directory = './unisys/static/audio_files/welcome'+str(i)+'.mp3'
	myobj.save(directory)

	return {'msgno':i, 'url':url_for('static', filename = 'audio_files/welcome'+str(i)+'.mp3')}


@app.route('/signs', methods = ['GET', 'POST'])
def signs():
	return render_template('signs.html')


'''
@app.route('/webrtc2', methods = ['GET', 'POST'])
def webrtc2():
	return render_template('webrtc2.html')
'''


############################################################################################################################################
#################    SOCKET-IO ROUTES    ###################################################################################################
############################################################################################################################################

@socketio.on('private message', namespace = '/private')
def handle_private_msg(payload):
	print(str(payload))
	#recipient_session_id = users[payload['username']]
	receiver = payload['receiver']
	message = payload['message']
	sender = payload['sender']
	room = payload['room']
	msgDB = MessageHistory(roomName = room, sender = sender, receiver = receiver, message = message)
	db.session.add(msgDB)
	db.session.commit()
	emit('new private message', (message, sender), room = room, namespace = '/private')


@socketio.on('connect', namespace = '/private')
def handle_connect():
	if current_user.is_authenticated:
		username = current_user.usn
		emit('user logged in', username, namespace = '/private')
		users[username] = request.sid
		print(username+' has logged in to the server with session id '+users[username])


@socketio.on('create or join room', namespace = '/private')
def handle_join_or_create_room(payload):
	print(str(payload))
	local = payload['localUser']
	remote = payload['remoteUser']
	found = 0
	#roomObjects = MessageHistory.query.distinct(MessageHistory.roomName).all()
	#rooms = [row.roomName for row in roomObjects]
	rooms = MessageHistory.query.with_entities(MessageHistory.roomName).distinct()
	print(rooms)
	for roomVal in rooms:
		print(roomVal)
		if local in roomVal and remote in roomVal:
			found = 1
			join_room(roomVal)
			print(local+' has joined the room '+roomVal+' with '+remote)
			emit('joined room', roomVal, room = roomVal, namespace = '/private')
			break

	if found == 0:
		roomVal = local+'&&&'+remote
		#rooms.append(roomVal)
		join_room(roomVal)
		print(local+' has joined the room '+roomVal+' with '+remote)
		emit('joined room', roomVal, room = roomVal, namespace = '/private')


@socketio.on('connect')
def handle_connect_default_namespace():
	print('default namespace is activated')