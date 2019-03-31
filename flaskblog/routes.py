from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")

def home():
	# grabbing all the post from the database
	posts = Post.query.all()
	return render_template ('home.html', posts=posts)

# getting user input and save it in database
@app.route("/register", methods=['GET', 'POST'])
def register():
	# if user is already logged in, it will redirect to home page
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password= hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! Go ahead and log in!', 'success')
		return redirect(url_for('login'))
	return render_template ('register.html', title= 'Register', form=form)

# checking the user input with database to log in
@app.route("/login", methods=['GET', 'POST'])
def login():
	# if user is already logged in, it will redirect to home page
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	#checking if the username and password typed matche the ones on the database
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			#if next page exists then redirect to that page, but if not, redirect to the home page
			return redirect(next_page) if next_page else redirect(url_for('home'))
		#if it does not match, it will simply show the message
		else:
			flash('Incorrect username or password', 'danger')

	return render_template ('login.html', title= 'Login', form=form)

# users can log out
@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

# users can see their account after creating and logging in
@app.route("/account")
@login_required
def account():

	return render_template ('account.html', title= 'Account')


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		# adding the post to the database
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success' )
		return redirect(url_for('home'))
	return render_template ('create_post.html', title= 'New Post', form=form)






