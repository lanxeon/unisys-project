from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,RadioField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from unisys.models import User

class Registration(FlaskForm):
	fname = StringField('First Name', validators = [DataRequired()])
	lname = StringField('Last Name', validators = [DataRequired()])
	usn=StringField('Username', validators=[DataRequired(), Length(min=3,max=15)])
	email=StringField('Email', validators=[DataRequired(), Email()])
	pwd=PasswordField('Password', validators=[DataRequired(), Length(min=8,max=15)])
	repwd=PasswordField('Confirm Password', validators=[DataRequired(), Length(min=5,max=15),EqualTo('pwd')])
	submit=SubmitField('Register')

	def validate_email(self, email):
		user=User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Already registered with the specified email')

	def validate_usn(self, usn):
		user=User.query.filter_by(usn=usn.data).first()
		if user:
			raise ValidationError('Username already taken. Please choose another one')


class Login(FlaskForm):
	email=StringField('Email', validators=[DataRequired(), Email()])
	pwd=PasswordField('Password', validators=[DataRequired(), Length(min=5,max=15)])
	remember=BooleanField('Remember me')
	submit=SubmitField('Log in')


# class Chat(FlaskForm):
# 	receiver = StringField('Receiver :', validators = [DataRequired()])
# 	submitRecv = SubmitField('Connect!')

# 	def validate_receiver(self, receiver):
# 		rcvr = User.query.filter_by(usn = receiver.data).first()
# 		if rcvr:
# 			pass
# 		else:
# 			raise ValidationError('Invalid receiver')