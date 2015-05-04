#some imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

#configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'se2015'
USERNAME = 'admin'
PASSWORD = 'root'

#something about initializing
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    return render_template('layout.html')

@app.route('/payment/<int:orderId>', methods=['POST'])
def add_payment(orderId):
    g.db.execute('insert into payment(orderId, creditcard, Month, Year, seccode, zip) values (?, ?, ?, ?, ?)',
                  [request.form['orderId'], request.form['creditcard'], request.form['Month'], request.form['Year'], request.form['seccode'], request.form['zip']])
    g.db.commit()
    flash('Thanks for your order')
    return render('layout.html')

@app.route('/add_order', methods=['GET','POST'])
def add_order():
   # if not session.get('logged_in'):
    #    abort(401)
    g.db.execute('insert into pizzaorder(piesize, premade, toppings, name, phone, message) values (?, ?, ?, ?, ?, ?, ?)',
                  [request.form['piesize'], request.form['premade'], request.form['toppings'], request.form['name'], request.form['phone'], request.form['message']])
    g.db.commit()
    flash('pizza ordered')
    return render_template('Payment.html', )

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
            return redirect(url_for('pizzabig.html'))
    return render_template('pizzabig.html', error=error)

@app.route('/guest', methods=['GET','POST'])
def guest():
    error = None
    #if request.method == 'POST':
    #    if request.form['guest'] != app.config['GUEST']:
    #      error = 'Please login or choose guest'
    #    else:
    session['logged_in'] = True
    flash('Welcome Guest')
    return redirect(url_for('show_entries'))
    return render_template('guest.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__== '__main__':
    app.run()


