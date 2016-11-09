import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, flash, session

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = 'this_is_a_secret'

DATABASEURI = "postgresql://sks2200:Databases2016**@w4111vm.eastus.cloudapp.azure.com/w4111"
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/SignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/SignIn')
def showSignIn():
    return render_template('signin.html')

@app.route('/userIndex')
def userIndex():
    return render_template('userIndex.html')

@app.route('/logout')
def logout():
    session.pop('user',None)
    flash("Logged out successfully!", category='success')
    return redirect('/')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    _username = request.form["username"]
    _password = request.form["password"]
    cursor = g.conn.execute("select password from users where username='"+_username+"';")
    for result in cursor:
      if (_password == result['password']):
        flash("Logged in successfully!", category='success')
        cursor.close()
        return redirect('/userIndex')
      else:
        flash("Wrong username or password!", category='error')
        cursor.close()
        return redirect('/SignIn')
    flash("Username not found!", category='error')
    cursor.close()
    return redirect('/SignUp')

@app.route('/validateSignUp',methods=['POST'])
def validateSignUp():
    _username = request.form["username"]
    _password = request.form["password"]
    _age = request.form["age"]
    _gender = request.form.get("gender")
    cursor = g.conn.execute("select username from users where username='"+_username+"';")

    for result in cursor:
      if (_username == result['username']):
        flash("Username already taken, please choose another.", category='error')
        cursor.close()
        return redirect('/SignUp')
    g.conn.execute("insert into users (username,password,age,gender) values('"+_username+"','"+_password+"',"+_age+",'"+_gender+"');")
    flash("Sign Up successful! Please Sign In", category='success')
    cursor.close()
    return redirect('/SignIn')


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
