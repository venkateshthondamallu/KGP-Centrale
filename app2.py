from flask import Flask, render_template,flash, request,session,redirect,g,url_for
import pymysql
import os
app = Flask(__name__)
app.secret_key = os.urandom(34)

@app.route('/')
def landing():
	return render_template('signup')

@app.route('/signup', methods=['GET', 'POST'])
def index():
	connection=pymysql.connect(host='127.0.0.1', user="bubby", password="bubby@123", db="flaskapp", charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)
	cursor = connection.cursor()
	if request.method == 'POST':
		
		username=request.form['username']
		email = request.form['email']
		password = request.form['password']
		confirmpassword = request.form['confirmpassword']
		if username:
			query = "SELECT password FROM signup WHERE username=%s"
			cur = cursor.execute(query, (username))
			if cur:
				flash('username already exists')
				return redirect(url_for('signup.html'))
			else:

				if confirmPassword == password:	
					try:
						query = "INSERT INTO signup (username,email,password,confirmpassword) VALUES (%s, %s, %s, %s)"
						cursor.execute(query, (username, email,password,confirmpassword))
						connection.commit()
					finally:
						connection.close()
					return redirect(url_for('login'))
				else:
					flash("Passwords do not match!")
					return redirect(url_for('signup.html'))
					
	else:
		return "error"
@app.route('/cabsharesearch', methods=['GET', 'POST'])
def cabsharesearch():
	if g.user:
		connection = pymysql.connect(host="127.0.0.1", user="bubby", password="bubby@123", db='flaskapp',
								   charset='utf8mb4',
								   cursorclass=pymysql.cursors.DictCursor)
		cursor = connection.cursor()
		query = 'SELECT cities FROM city_dropdown'
		cursor.execute(query)
		cities = cursor.fetchall()
		connection.commit()

		if request.method=='POST':
			Username = request.form['Username']
			mobilenumber = request.form['mobilenumber']
			Date=request.form['Date']
			Time=request.form['Time']
			From=request.form['From']
			To=request.form['To']

			query1='SELECT * FROM cabsharing WHERE Date=' + Date
			cursor.execute(query1)
			connection.commit()
			result = cursor.fetchall()
			print(result)

		return render_template('cabsharing.html', cities=cities)

	else:
		return redirect(url_for('login'))

@app.route('/vehicles')
def vehicles():
	if g.user:
		connection = pymysql.connect(host="127.0.0.1", user="bubby", password="bubby@123", db='flaskapp',
								   charset='utf8mb4',
								   cursorclass=pymysql.cursors.DictCursor)
		cursor = connection.cursor()
		
		query='SELECT COUNT(*) FROM vehicles'
		cursor.execute("SELECT COUNT(*) FROM vehicles")
		connection.commit()
		result=cursor.fetchone()
		print(result[0])
		return "1"


	else:
		return redirect('login')				


							
		
			
		
	
#password = "SELECT * from signup()

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		session.pop('username',None)
		if request.form['password'] =='password':
			session['username'] = request.form['username']
			return redirect(url_for('protected'))

	return render_template('login.html')
@app.route('/logout')
def logout():
	return redirect(url_for('login'))	

@app.route('/homepage',methods = ['GET','POST'])
def homepage():
	if g.username:	
		return render_template('homepage.html')

	return render_template('login.html')	


@app.before_request
def before_request():
	g.username = None
	if 'username' in session:
		g.username = session['user']

@app.route('/getsession')
def getsession():
	if 'username' in session:
		return session['username']

	return "Fucker Not logged in"

@app.route('/dropsession')
def dropsession():
	session.pop('username',None)
	return "Fuckin Dropped!"


@app.route('/cabsharing',methods = ['GET','POST'])
def cabsharing():
	return render_template('cabsharing.html')
if __name__ == "__main__":

	app.run(port = '9999',debug=True)