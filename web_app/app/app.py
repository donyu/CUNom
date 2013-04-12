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

def get_favorites():
    cursor = con.cursor()
    cursor.prepare(
        """
        select e.e_id, e.name, e.dateof from Users u, favorited f, Events e 
        where u.username = f.username and f.e_id = e.e_id and u.username = :session_user
        """
        )
    cursor.execute(None, {'session_user':session['username']})
    return cursor.fetchall()

def get_squestions():
    cursor = con.cursor()
    cursor.prepare(
        """
        select sq.q_id, sq.question, sq.answer from SecurityQuestions sq, Users u 
        where u.username = sq.username and u.username = :session_user
        """
        )
    cursor.execute(None, {'session_user':session['username']})
    return cursor.fetchall()

def get_lprefs():
    cursor = con.cursor()
    cursor.prepare(
        """
        select distinct pl.p_id, pl.l_id, l.name from 
        Preferences p, Locations l, preferredLocations pl, Users u, hasPreferences hp
        where pl.p_id = p.p_id and pl.l_id = l.l_id and p.p_id = hp.p_id and hp.username = :session_user 
        """
        )
    cursor.execute(None, {'session_user':session['username']})
    return cursor.fetchall()

def get_eprefs():
    cursor = con.cursor()
    cursor.prepare(
        """
        select distinct el.p_id, el.e_id, e.name from 
        Preferences p, Events e, preferredEvents el, Users u, hasPreferences hp
        where el.p_id = p.p_id and el.e_id = e.e_id and p.p_id = hp.p_id and hp.username = :session_user 
        """
        )
    cursor.execute(None, {'session_user':session['username']})
    return cursor.fetchall()

@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        friends = get_friends()
        favorites = get_favorites()
        return render_template('index.html', name = session['username'], friends = friends, favorites = favorites)
    l_form = LoginForm()
    return render_template('login.html', **{'l_form':l_form})

@app.route('/preferences')
def preferences():
    session['username'] = "don8yu"
    if 'username' in session:
        e_prefs = get_eprefs()
        l_prefs = get_lprefs()
        s_questions = get_squestions()
        # subscribed = is_user_subscribed()
        # return render_template('preferences.html', name = session['username'], e_prefs = e_prefs, l_prefs = l_prefs, s_questions = s_questions, subscribed = subscribed)
        return render_template('preferences.html', name = session['username'], s_questions = s_questions, l_prefs = l_prefs)
    return redirect('/')

@app.route('/delete_lpref/<p_id>/<l_id>')
def delete_lpref(p_id, l_id):
    # delete friend relationship from database
    cursor = con.cursor()
    cursor.prepare('delete from preferredLocations where p_id = :p_id and l_id = :l_id')
    cursor.execute(None, {'p_id':p_id, 'l_id':l_id})
    con.commit()

    # redirect back to previous page
    return redirect('/preferences')

@app.route('/delete_epref/<p_id>/<e_id>')
def delete_epref(p_id, e_id):
    # delete friend relationship from database
    cursor = con.cursor()
    cursor.prepare('delete from preferredEvents where p_id = :p_id and e_id = :e_id')
    cursor.execute(None, {'p_id':p_id, 'e_id':l_id})
    con.commit()

    # redirect back to previous page
    return redirect('/preferences')

@app.route('/delete_question/<question_id>')
def delete_question(question_id):
    # delete friend relationship from database
    cursor = con.cursor()
    cursor.prepare('delete from SecurityQuestions where q_id = :delete_question and username = :session_user')
    cursor.execute(None, {'delete_question':question_id, 'session_user':session['username']})
    con.commit()

    # redirect back to previous page
    return redirect('/preferences')

@app.route('/delete_friend/<friend_name>')
def delete_friend(friend_name):
    # delete friend relationship from database
    cursor = con.cursor()
    cursor.prepare('delete from friends_with where person_2 = :delete_friend and person_1 = :session_user')
    cursor.execute(None, {'delete_friend':friend_name, 'session_user':session['username']})
    con.commit()

    # redirect back to previous page
    return redirect('/')

@app.route('/delete_favorite/<favorite_id>')
def delete_favorite(favorite_id):
    # delete favorited relationship from database
    cursor = con.cursor()
    cursor.prepare('delete from favorited where e_id = :delete_favorite and username = :session_user')
    cursor.execute(None, {'delete_favorite':favorite_id, 'session_user':session['username']})
    con.commit()

    # redirect back to previous page
    return redirect('/')

@app.route('/add_question', methods=['POST'])
def add_question():
    # add friend relationship from database
    cursor = con.cursor()
    # need to figure out next id for this question
    cursor.execute('select max(q_id) from SecurityQuestions')
    new_id = int(cursor.fetchone()[0]) + 1
    cursor.prepare('insert into SecurityQuestions values(:new_id, :question, :answer, :session_user)')
    cursor.execute(None, {'new_id':new_id, 'question':request.form['question'], 'answer':request.form['answer'], 'session_user':session['username']})
    con.commit()

    # redirect back to previous page
    return redirect('/preferences')

@app.route('/add_friend', methods=['POST'])
def add_friend():
    # add friend relationship from database
    cursor = con.cursor()
    cursor.prepare('insert into friends_with values(:session_user, :add_friend)')
    cursor.execute(None, {'add_friend':request.form['username'], 'session_user':session['username']})
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

#event search form
@app.route('/search')
def search():
    return render_template('search.html')

#event listings page
@app.route('/food', methods=['GET', 'POST'])
def food():
    session['username'] = "don8yu"
    events = []
    if 'username' in session:
        if request.method == 'POST':
            print 'hi'
            keyword = request.form['query_term']
            tag = request.form['query_tag']
            location = request.form['query_location']
            date = request.form['query_date']
            events = get_events(keyword, tag, location, date)
        else:
            events = get_events("", "", "", "")
    return render_template('listings.html', name = session['username'], events = events)

def get_events(keyword, tag, location, dateof):
    cursor = con.cursor()
    cursor.execute(
    """
    select distinct 
        Events.name, Events.description, Events.dateof, Tags.tag_name, Locations.name
    from 
        Events, Tags, tagged_with, Locations, located
    where 
        Events.e_id = tagged_with.e_id 
        and Tags.tag_name = tagged_with.tag_name
        and Locations.l_id = located.l_id

        and Events.name like :keyword
        and Tags.tag_name like :tag
        and Locations.name like :location
        and Events.dateof like :dateof
    """,
    keyword = '%' + keyword + '%',
    tag = '%' + tag + '%',
    location = '%' + location + '%',
    dateof = '%' + dateof + '%'
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
