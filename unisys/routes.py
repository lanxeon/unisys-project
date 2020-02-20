from flask import render_template, url_for, request, redirect, flash, request, session
from unisys import app, lm, bcrypt, db, socketio
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import send, emit
import os
from unisys.forms import Registration, Login
from unisys.models import User

users = {}

@app.route('/')
@app.route('/home')
def home():
	full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'unisys_logo.jpg')
	full_filename1 = os.path.join(app.config['UPLOAD_FOLDER'], 'abstract2.jpg')
	full_filename2 = os.path.join(app.config['UPLOAD_FOLDER'], 'capacity.jpg')
	full_filename3 = os.path.join(app.config['UPLOAD_FOLDER'], 'cover1.jpg')
	full_filename4 = os.path.join(app.config['UPLOAD_FOLDER'], 'pp1.png')
	full_filename5 = os.path.join(app.config['UPLOAD_FOLDER'], 'tp-01-02.jpeg')
	return render_template('home.html',user_image = full_filename,user_image1 = full_filename1,user_image2 = full_filename2,user_image3 = full_filename3,user_image4 = full_filename4,bg_image = full_filename5)


@app.route('/about')
def about():
    return '<h1>About Page</h1>' 


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
		flash(f'Registered successfully', 'success')
		return redirect(url_for('login'))

	return render_template('register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = Login()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user and bcrypt.check_password_hash(user.pwd , form.pwd.data):
			login_user(user, remember=form.remember.data)
			#socketio.send('connect', user.usn, namespace = '/private')
			flash(f'Registered successfully', 'success')
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))

	return render_template('login.html', form = form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route('/chat')
@login_required
def chat():
	return render_template('chat.html')


@app.route('/account')
@login_required
def account():
	return render_template('account.html')



########################################################################################################################
#####     SOCKET-IO ROUTES    #####
########################################################################################################################

@socketio.on('message')
def handle_msg(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)


@socketio.on('private message', namespace = '/private')
def handle_private_msg(payload):
	recipient_session_id = users[payload['username']]
	message = payload['message']
	emit('new private message', message, room=recipient_session_id)
	
'''
@socketio.on('user joined', namespace = '/private')
def handle_user_joined(sock_usn):
	users[sock_usn] = request.sid
	print(sock_usn+' has logged in to the server')
'''

@socketio.on('connect', namespace = '/private')
def handle_connect():
	if current_user.is_authenticated:
		username = current_user.usn
		emit('user logged in', username, namespace = '/private')
		users[username] = request.sid
		print(username+' has logged in to the server with session id '+users[username])