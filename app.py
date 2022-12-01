import sqlite3
from flask import Flask, request, render_template, session, redirect
from markupsafe import escape
import db


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xecasfsaf345ewe*)*5vd/'

@app.route("/")
def index():
	data={'title': 'Dashboard'}
	if  session.get('email'):
		data['email'] = session['email']
	return render_template('index.html', data=data)

@app.route("/register", methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		return do_the_register()
	else:
		return show_the_register_form()

@app.route("/main")
def main():
	return """
		<!DOCTYPE html>
		<html>
			<head>
				<title>Page Title</title>
			</head>
			<body>
				<h1>My First Heading</h1>
				<p>My first paragraph.</p>
				<a href="/">Home</a>
			</body>
		</html>
		"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

def do_the_login():
	print(request.form)
	email = request.form['email']
	password = request.form['password']
	if db.check_account(email, password):
		session['email'] = email
		return redirect('/')
	else:
		return render_template('login.html', title='Log In', error='Invalid Login. Please try again')

def show_the_login_form():
	return render_template('login.html', title='Log In')

def show_the_register_form():
	return render_template('register.html', title='Register')

def do_the_register():
	print(request.form)
	email = request.form['email']
	password = request.form['password']
	password1 = request.form['password1']
	if password == password1:
		try:
			db.create_account(email, password)
			session['email'] = email
			return redirect('/')
		except sqlite3.IntegrityError:
			return render_template('register.html', title='Register', error='Email already exists')
	else:
		return render_template('register.html', title='Register', error='Passwords do not match')
	
@app.route('/logout')
def logout():
	#session.pop('email', None)
	session.clear()
	return redirect('/')