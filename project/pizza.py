#some imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from flaskext.mysql import MySQL

#Database stuff
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'bigbigpizza'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#configuration
DEBUG = True
SECRET_KEY = 'se2015'
USERNAME = 'admin'
PASSWORD = 'root'

#something about initializing
#app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#def connect_db():
#    return sqlite3.connect(app.config['DATABASE'])

#def init_db():
#    with closing(connect_db()) as db:
#        with app.open_resource('schema.sql', mode='r') as f:
#            db.cursor().executescript(f.read())
#        db.commit()

#@app.before_request
#def before_request():
#    g.db = connect_db()

#@app.teardown_request
#def teardown_request(exception):
#    db = getattr(g, 'db', None)
#    if db is not None:
#        db.close()
@app.route('/createuser')
def add_user():
    
         
@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries(title, text) values (?, ?)',
                  [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was succesfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        if request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/guest', methods=['GET','POST'])
def guest():
    error = None
    session['logged_in'] = True
    flash('Welcome Guest')
    return render_template('guest.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('layout'))


if __name__== '__main__':
    app.run()


