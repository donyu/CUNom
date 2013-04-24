import cx_Oracle
from flask import Flask, flash, render_template, redirect, request, session
from wtforms import Form, SelectMultipleField, BooleanField, TextField, PasswordField, validators, widgets, RadioField

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

def get_locations():
    cursor = con.cursor()
    cursor.execute('select name from Locations ')
    locations = cursor.fetchall()
    locations = [(l[0], l[0]) for l in locations]
    return locations

def get_tags():
    cursor = con.cursor()
    cursor.execute('select tag_name from Tags ')
    tags = cursor.fetchall()
    tags = [(t[0], t[0]) for t in tags]
    return tags

# login form here
class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')
    
class SearchForm(Form):
    query_term = TextField('query_term', default='')
    # query_tag = TextField('query_tag', default='')
    query_tag = SelectMultipleField('query_location', choices=get_tags())
    # query_location = TextField('query_location', default='')
    query_location = SelectMultipleField('query_location', choices=get_locations())
    query_date = TextField('query_date', default='')

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

def get_p_id():
    cursor = con.cursor()
    cursor.execute("""
        select p.p_id from Preferences p, hasPreferences hp, Users u
        where u.username = :session_user and hp.username = u.username
        and p.p_id = hp.p_id
        """, session_user = session['username'])
    return cursor.fetchone()[0]

def is_user_subscribed():
    cursor = con.cursor()
    cursor.prepare(
        """
        select subscribed from Users u, has h, Emails e 
        where u.username = :session_user and h.username = u.username and h.address = e.address
        """
        )
    cursor.execute(None, {'session_user':session['username']})
    return cursor.fetchone()

def get_email():
    cursor = con.cursor()
    cursor.prepare(
        """
        select e.address from Users u, has h, Emails e 
        where u.username = :session_user and h.username = u.username and h.address = e.address
        """
        )
    cursor.execute(None, {'session_user':session['username']})
    return cursor.fetchone()

def get_p_on_off():
    cursor = con.cursor()
    cursor.execute("""
        select p.on_or_off from Preferences p, hasPreferences hp, Users u
        where u.username = :session_user and hp.username = u.username
        and p.p_id = hp.p_id
        """, session_user = session['username'])
    return cursor.fetchone()[0]

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
    if 'username' in session:
        e_prefs = get_eprefs()
        l_prefs = get_lprefs()
        s_questions = get_squestions()
        subscribed = is_user_subscribed()
        print subscribed
        p_on_off = get_p_on_off()
        email = get_email()
        return render_template('preferences.html', name = session['username'], p_on_off = p_on_off, s_questions = s_questions, l_prefs = l_prefs, e_prefs = e_prefs, email = email, subscribed = subscribed)
    return redirect('/')

@app.route('/change_email', methods = ['POST'])
def change_email():
    email = request.form['email']
    past_email = get_email()[0]
    subscribed = request.form['subscribed_select']
    if subscribed == "Yes":
        subscribed = 1
    else:
        subscribed = 0

    # check if these settings already exist
    cursor = con.cursor()
    cursor.prepare('select address, subscribed from Emails where address = :email')
    cursor.execute(None, {'email':email})
    if cursor.fetchone():
        cursor.execute('update Emails set subscribed = :subscribed where address = :email', email=email, subscribed=subscribed)
        return redirect('/preferences')

    # change email settings for user
    cursor.prepare('insert into Emails values(:email, :subscribed)')
    cursor.execute(None, {'email':email, 'subscribed':subscribed})

    # now we change has table
    cursor.prepare('update has set address = :email where username = :username')
    cursor.execute(None, {'email':email, 'username':session['username']})
    cursor.prepare('delete from Emails where address = :past_email')
    cursor.execute(None, {'past_email':past_email})
    con.commit()

    return redirect('/preferences')

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
    cursor.execute(None, {'p_id':p_id, 'e_id':e_id})
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

@app.route('/add_favorite/<e_id>')
def add_favorite(e_id):
    cursor = con.cursor()
    cursor.execute('select e_id from favorited where e_id = :e_id and username = :session_user', session_user = session['username'], e_id = e_id)
    if cursor.fetchone():
        flash('You have already favorited this event')
        return redirect('/food')
    cursor.prepare('insert into favorited values(:session_user, :e_id)')
    cursor.execute(None, {'session_user':session['username'], 'e_id':e_id})
    con.commit()

    # redirect back to previous page
    return redirect('/food')

@app.route('/add_lpref/<l_id>')
def add_lpref(l_id):
    cursor = con.cursor()
    p_id = get_p_id()
    cursor.execute('select p_id, l_id from preferredLocations where l_id = :l_id and p_id = :p_id', p_id = p_id, l_id = l_id)
    if cursor.fetchone():
        flash('You have already saved this as an location preference')
        return redirect('/food')
    cursor.prepare('insert into preferredLocations values(:p_id, :l_id)')
    cursor.execute(None, {'p_id':p_id, 'l_id':l_id})
    con.commit()

    # redirect back to previous page
    return redirect('/food')

@app.route('/update_p_on_off/<on_off>')
def update_p_on_off(on_off):
    cursor = con.cursor()
    p_id = get_p_id()
    cursor.prepare('update Preferences set on_or_off = :on_off where p_id = :p_id')
    cursor.execute(None, {'p_id':p_id, 'on_off':on_off})
    con.commit()

    # redirect back to previous page
    return redirect('/preferences')

@app.route('/add_epref/<e_id>')
def add_epref(e_id):
    cursor = con.cursor()
    p_id = get_p_id()
    cursor.execute('select e_id, p_id from preferredEvents where e_id = :e_id and p_id = :p_id', p_id = p_id, e_id = e_id)
    if cursor.fetchone():
        flash('You have already saved this as an event preference')
        return redirect('/food')
    cursor.prepare('insert into preferredEvents values(:p_id, :e_id)')
    cursor.execute(None, {'p_id':p_id, 'e_id':e_id})
    con.commit()

    # redirect back to previous page
    return redirect('/food')

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
    cursor.execute('select username from Users where username = :friend', friend = request.form['username'])
    if not cursor.fetchone():
        flash('This user does not exist. Ask your friend for his real username')
        return redirect('/')
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

#event listings page
@app.route('/food', methods=['GET', 'POST'])
def food():
    events = []
    if 's_form' not in session:
        session['s_form'] = SearchForm()
    if request.method == 'POST':
        session['s_form'] = SearchForm(request.form)
    s_form = session['s_form']
    keyword = s_form.query_term.data
    tag = s_form.query_tag.data
    location = s_form.query_location.data
    date = str(s_form.query_date.data).upper()

    events = get_events(keyword, tag, location, date)
    events = [list(e) for e in events]
    for event in events:
        tags = get_tags(event)
        event.append(tags)
    if 'username' in session:
        return render_template('listings.html', name = session['username'], events = events, s_form = session['s_form'])
    else:
        l_form = LoginForm()
        return render_template('listings.html', events = events, l_form = l_form, s_form = session['s_form'])


def get_tags(event):
    cursor = con.cursor()
    cursor.execute(
        """
        select t.tag_name from Tags t, Events e, tagged_with tw 
        where e.e_id = tw.e_id and tw.tag_name = t.tag_name and e.e_id = :e_id
        """,
        e_id = event[4]
        )
    return cursor.fetchall()

def get_events(keyword, tag, location, dateof):
    cursor = con.cursor()
    query_str = """
    select 
        Events.name, Events.description, Events.dateof, Locations.name, Events.e_id, Locations.l_id, Locations.address, Locations.directions
    from 
        Events, Tags, tagged_with, Locations, located
    where
        Events.e_id = tagged_with.e_id 
        and Tags.tag_name = tagged_with.tag_name
        and Locations.l_id = located.l_id
        and located.e_id = Events.e_id
    """
    query_str += "and (Events.name like :keyword or Events.description like :keyword) "
    if tag:
        query_str += "and Tags.tag_name in "
        query_str += "("
        for t in tag[:len(tag) - 1]:
            query_str += ":" + t.split()[0] + ", "
        query_str += ":" + tag[len(tag) - 1].split()[0]
        query_str += ") "
    if location:
        query_str += "and Locations.name in "
        query_str += "("
        i = 0
        for l in location[:len(location) - 1]:
            query_str += ":" + l.split()[0] + str(i) + ", "
            i += 1
        query_str += ":" + location[len(location) - 1].split()[0] + str(i)
        query_str += ") " 
    query_str += "and Events.dateof like :dateof"
    query_str += " group by Events.name, Events.description, Events.dateof, Locations.name, Events.e_id, Locations.l_id, Locations.address, Locations.directions"
    print query_str
    cursor.prepare(query_str)
    c_args = {}
    c_args['keyword'] = '%' + keyword + '%'

    if tag:
        for t in tag:
            c_args[t.split()[0]] = t
    if location:
        i = 0
        for l in location:
            c_args[l.split()[0] + str(i)] = l
            i += 1
    c_args['dateof'] = '%' + dateof + '%'
    print c_args
    cursor.execute(None, c_args)
    return cursor.fetchall()

@app.route('/logout')
def logout():
    del session['username']
    if 's_form' in session:
        del session['s_form']
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

        # insert into Preferences table
        signup_cursor.execute('select max(p_id) from Preferences')
        new_id = int(signup_cursor.fetchone()[0]) + 1
        signup_cursor.execute('insert into Preferences values(:p_id, :on_or_off)', p_id = new_id, on_or_off = 0)
        signup_cursor.execute('insert into hasPreferences values(:username, :p_id)', username = request.form['username'], p_id = new_id)

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
