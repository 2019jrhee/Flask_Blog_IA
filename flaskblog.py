from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm 
from datetime import datetime



app = Flask(__name__)
#for security
app.config['SECRET_KEY'] = '0688991dd4efef8f189cf116e83258ef'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# database setup
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(80), unique=True, nullable=False)
	#image_file = username = db.Column(db.String(20), nullable=False, default ='default.jpg') for line 20, put {self.image_file}
	password = db.Column(db.String(20), nullable=False)

	# get the author who created the post in the Post model
	posts = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.password}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


posts = [

	{ 'author': 'Michelle Rhee',
	  'title': 'Post 1',
	  'content': 'First content',
	  'date_posted': 'March 30, 2018'

	}
]

@app.route("/")
@app.route("/home")

def home():
    return render_template('home.html', posts = posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Welcome {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template ('register.html', title= 'Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.username.data == 'abcdef' and form.password.data == 'password':
			flash('Welcome Back!', 'success')
			return redirect(url_for('home'))
		#else:
			#flash('Incorrect username or password', 'danger')

	return render_template ('login.html', title= 'Login', form=form)

if __name__ =='__main__':
	app.run(debug=True)