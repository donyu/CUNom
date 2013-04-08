import cx_Oracle
from flask import Flask, render_template, redirect, request, session
# from wtfforms import Form, BooleanField, TextField, PasswordField, validators

app = Flask(__name__)

# connection string params
user = "dy2212"
pswd = "dophie"
host = "w4111f.cs.columbia.edu"
port = "1521"
sid = "ADB"
dsn = cx_Oracle.makedsn(host, port, sid)

# connect and test
con = cx_Oracle.connect(user, pswd, dsn)

# def username_free(form, field):

# class LoginForm(Form):
#     username = TextField('username', [validators.Required(), validators.Length(min=4, max=25), username_free])
#     password = PasswordField('password', [validators.Required(), validators.Length(min=7, max=25)])

@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html', name = session['username'])
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # test if username and password are in database
        cursor = con.cursor()
        cursor.prepare('select username, password from Users where username = :user_form and password = :pswd_form')
        cursor.execute(None, {'user_form':username, 'pswd_form':password})
        if cursor.fetchone():
            session['username'] = username
        return redirect('/')

@app.route('/food')
def food():
    return render_template('food.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/') 

@app.route('/signup', methods=['POST'])
def signup():
    # check if username taken or not
    cursor = con.cursor()
    cursor.prepare('select username from Users where username = :new_user')
    cursor.execute(None, {'new_user':request.form['username']})
    if cursor.fetchone():
        return 
    else:
        # if not taken then we create values in database
        signup_cursor = con.cursor()
        signup_cursor.prepare('insert into Users values(:new_user, :new_pass)')
        c_args = {}
        c_args['new_user'] = request.form['username']
        c_args['new_pass'] = request.form['password']
        signup_cursor.execute(None, c_args)
        # be sure to commit these inserts to db
        con.commit()
    
    # create a session now
    username = request.form['username']
    session['username'] = username
    return redirect('/')

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'l34GE0q1l1U+4D8c4S/1Yg=='
    app.run()
