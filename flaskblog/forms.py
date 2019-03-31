from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from flaskblog.models import User

# components for registering 
class RegistrationForm(FlaskForm):
	username = StringField('Username', 
		validators= [DataRequired(), Length(min=5, max=20)])
	email = StringField('Email', validators= [DataRequired(), Email()])

	password = PasswordField('Password', validators= [DataRequired()])

	#confirm_password = PasswordField('Confirm Password', validators= [DataRequired()])

	submit = SubmitField('Register')

	#def validate_username(self, username): put ValidationError next to Email on the top

		#user = User.query.filter_by(username=username.data).first()
		#if user:
			#raise ValidationError('This username already exists. Try a new one!')

	#def validate_email(self, email):

		#user = User.query.filter_by(email=email.data).first()
		#if user:
			#raise ValidationError('This email already exists. Try a new one!')

# components for logging in 
class LoginForm(FlaskForm):
	username = StringField('Username', 
		validators= [DataRequired(), Length(min=5, max=20)])


	password = PasswordField('Password', validators= [DataRequired()])

	
	submit = SubmitField('Log In')

class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()]) 
	submit = SubmitField('Post')
