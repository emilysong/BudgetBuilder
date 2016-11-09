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
  if 'username' in session:
    #incomes
    cursor1 = g.conn.execute("select uuid from users where username='"+session['username']+"';")
    for result1 in cursor1:
      uuid = result1['uuid']
    iids = []
    cursor2 = g.conn.execute("select iid from earns where uuid='"+str(uuid)+"';")
    for result2 in cursor2:
      iids.append(result2['iid'])
    incomes_list = []
    for iid in iids:
      cursor3 = g.conn.execute("select * from incomes_activities_earned_by where iid='"+str(iid)+"';")
      for result3 in cursor3:
        result_dict = {
        'Sum': result3['sum'],
        'Date': result3['date'],
        'Sector': result3['sector'],
        'Description': result3['description']
        }
        incomes_list.append(result_dict) 
    
    #purchases
    cursor4 = g.conn.execute("select uuid from users where username='"+session['username']+"';")
    for result4 in cursor4:
      uuid = result4['uuid']
    pids = []
    cursor5 = g.conn.execute("select pid from makes where uuid='"+str(uuid)+"';")
    for result5 in cursor5:
      pids.append(result5['pid'])
    purchases_list = []
    for pid in pids:
      cursor6 = g.conn.execute("select * from purchases_businesses_made_from where pid='"+str(pid)+"';")
      for result6 in cursor6:
        result_dict = {
        'Price': result6['price'],
        'Date': result6['date'],
        'Name': result6['name'],
        'Phone_Number': result6['phone_number'],
        'Address': result6['address'],
        'Industry': result6['industry'],
        'Category': result6['category'],
        'Item': result6['item']
        }
        purchases_list.append(result_dict) 

    #budgets
    cursor7 = g.conn.execute("select uuid from users where username='"+session['username']+"';")
    for result7 in cursor7:
      uuid = result7['uuid']
    budgets_list = []
    cursor8 = g.conn.execute("select * from budgetshas where uuid='"+str(uuid)+"';")
    for result8 in cursor8:
      result_dict = {
      'Period_Start': result8['period_start'],
      'Amount': result8['amount'],
      'Duration': result8['duration'],
      'Category': result8['category']
      }
      budgets_list.append(result_dict) 

    return render_template('userIndex.html', username=session['username'], incomes_list=incomes_list, purchases_list=purchases_list , budgets_list=budgets_list)
  else:
    return render_template("index.html")

@app.route('/SignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/SignIn')
def showSignIn():
    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully!", category='success')
    return redirect('/')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    _username = request.form["username"]
    _password = request.form["password"]
    cursor = g.conn.execute("select password from users where username='"+_username+"';")
    for result in cursor:
      if (_password == result['password']):
        session['username'] = _username
        flash("Logged in successfully!", category='success')
        cursor.close()
        return redirect('/')
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

@app.route('/addPurchase')
def addPurchase():
  if 'username' in session:
    return render_template('/addPurchase.html')
  else:
    flash("Please sign in to have access to that page", category='error')
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
