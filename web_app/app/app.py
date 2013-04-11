import cx_Oracle
from flask import Flask, flash, render_template, redirect, request, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators

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

# login form here
class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')
    
# functions to get manipulate database

def get_friends():
    cursor = con.cursor()
    cursor.prepare('select u.username from Users u, friends_with fw where u.username = fw.person_2 and fw.person_1 = :session_user')
    cursor.execute(None, {'session_user':session['username']})
    return cursor.fetchall()

@app.route('/')
@app.route('/index')
def index():
    session['username'] = "don8yu"
    if 'username' in session:
        friends = get_friends()
        return render_template('index.html', name = session['username'], friends = friends)
    l_form = LoginForm()
    return render_template('login.html', **{'l_form':l_form})

@app.route('/delete_friend/<friend_name>')
def delete_friend(friend_name):
    # delete friend relationship from database
    cursor = con.cursor()
    cursor.prepare('delete from friends_with where person_2 = :delete_friend and person_1 = :session_user')
    cursor.execute(None, {'delete_friend':friend_name, 'session_user':session['username']})
    con.commit()

    # redirect back to previous page
    return redirect('/')

@app.route('/add_friend', methods=['POST'])
def add_friend():
    # delete friend relationship from database
    cursor = con.cursor()
    cursor.prepare('insert into friends_with values(:session_user, :delete_friend)')
    cursor.execute(None, {'delete_friend':request.form['username'], 'session_user':session['username']})
    con.commit()

    # redirect back to previous page
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        # test if username and password are in database
        cursor = con.cursor()
        cursor.prepare('select username, password from Users where username = :user_form and password = :pswd_form')
        cursor.execute(None, {'user_form':username, 'pswd_form':password})
        if cursor.fetchone():
            session['username'] = username
        else:
            flash('Incorrect Login Credentials')
        return redirect('/')


"""
@app.route('/delete_friend/<friend_name>')
def delete_friend(friend_name):
    # delete friend relationship from database
    cursor = con.cursor()
    cursor.prepare('delete from friends_with where person_2 = :delete_friend and person_1 = :session_user')
    cursor.execute(None, {'delete_friend':friend_name, 'session_user':session['username']})
    con.commit()

    # redirect back to previous page
    return redirect('/')


td><a href="{{url_for('delete_friend', friend_name=friend[0]) }}">X</a></td>


"""
#event search form
@app.route('/search')
def search():
    return render_template('search.html')

#event listings page
@app.route('/food/<keywords>/<tags>/<location>/<date>')
def list(keywords, tags, location, date):
    session['username'] = "don8yu"
    if 'username' in session:
        events = get_events(keywords, tags, location, date)
        return render_template('listings.html', name = session['username'], events = events)


def get_events(keywords, tags, location, date):
    cursor = con.cursor()
    cursor.execute(
        """
        select *
        from Events
        """
        )
    #cursor.execute(None, {'session_user':session['username']})
    return cursor.fetchall()







@app.route('/logout')
def logout():
    del session['username']
    return redirect('/') 

@app.route('/signup', methods=['POST'])
def signup():
    # check if password long enough
    if len(request.form['password']) < 4:
        flash('Password must be more than 3 characters')
        return redirect('/')
    # check if username taken or not
    cursor = con.cursor()
    cursor.prepare('select username from Users where username = :new_user')
    cursor.execute(None, {'new_user':request.form['username']})
    if cursor.fetchone():
        flash('Username already taken')
        return redirect('/')
    else:
        # if not taken then we create values in database
        signup_cursor = con.cursor()

        # insert to User table
        signup_cursor.prepare('insert into Users values(:new_user, :new_pass)')
        c_args = {}
        c_args['new_user'] = request.form['username']
        c_args['new_pass'] = request.form['password']
        signup_cursor.execute(None, c_args)

        # insert to Emails table
        signup_cursor.prepare('select address from Emails where address = :new_email')
        signup_cursor.execute(None, {'new_email':request.form['email']})
        if signup_cursor.fetchone():
            flash('Email is already associated with another User')
            return redirect('/')
        signup_cursor.prepare('insert into Emails values(:new_email, 0)')
        signup_cursor.execute(None, {'new_email':request.form['email']})

        # insert to has table
        signup_cursor.prepare('insert into has values(:new_user, :new_email)')
        c_args = {}
        c_args['new_user'] = request.form['username']
        c_args['new_email'] = request.form['email']
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
