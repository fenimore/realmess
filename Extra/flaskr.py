# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

from . import app, db
from .models import User, Contract, Submission

# Routes
@app.route('/')
def index():
    return render_template('index.html')
        
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_user = User(request.form['username'],request.form['email'], request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        session['logged_in'] = True
        session['username'] = request.form['username']
        flash('New user was successfully added')
        return redirect(url_for('index'))
    return render_template('signup.html')
    
@app.route('/users')
def show_users():
    users = []
    user_query = User.query.all()
    for user in user_query:
        this_user = {'username':user.username, 'email':user.email, 'password':user.password}
        users.append(this_user)
    #flash(users[0]['username'])
    return render_template('users.html', users=users)

@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    profile = {'username':user.username, 'email':user.email, 'password':user.password}
    return render_template('profile.html', user=profile)

@app.route('/profile')
def my_profile():
    me = session['username']
    user = User.query.filter_by(username=me).first()
    profile = {'username':user.username, 'email':user.email, 'password':user.password}
    return render_template('profile.html', user=profile)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        pwd = request.form['password']
        user = User.query.filter_by(username=request.form['username']).first()
        #flash(pwd)
        if pwd == user.password:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('You are logged in')
            return redirect(url_for('index'))
        else:
            error = 'Invalid entry'
    return render_template('login.html', error=error)
    

@app.route('/logout')
def logout():
    # The pop doesn't do anything if the user isn't logged it.
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/oblige', methods=['GET', 'POST'])
def oblige():
    error = None
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        new_contract= Contract(request.form['title'], request.form['body'], request.form['end_date'], request.form['user_1'], request.form['user_2'])
        db.session.add(new_contract)
        db.session.commit()
        flash('New Contract was successfully posted')
        return redirect(url_for('show_contracts'))     
    else:
        error = 'Invalid entry'            
    users = []
    user_query = User.query.all()
    for user in user_query:
        this_user = {'username':user.username}
        users.append(this_user)
    return render_template('add_contract.html', users=users)   

@app.route('/contracts')
def show_contracts():
    contracts = []
    contracts_query = Contract.query.all()
    for contract in contracts_query:
        this_contract = {"title":contract.title, "end_date":contract.end_date, 'body':contract.body,'user_1':contract.user_1,'user_2':contract.user_2}
        contracts.append(this_contract)
    return render_template('show_contracts.html', contracts=contracts)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    error = None
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        c = Contract.query.filter_by(id=request.form['contract']).first()
        new_submission= Submission(request.form['title'], request.form['body'], c, request.form['author'])
        db.session.add(new_submission)
        db.session.commit()
        flash('Submission complete')
        return redirect(url_for('index'))     
    else:
        error = 'Invalid entry' 
    contracts = []
    contract_query = Contract.query.all()
    for contract in contract_query:
        this_contract = {'title':contract.title, 'id':contract.id}
        contracts.append(this_contract)
    return render_template('submit.html', contracts=contracts)   
    

@app.route('/bulliten')
def show_entries():
    posts = []
    posts_query = Post.query.all()
    for post in posts_query:
        this_post = {'title':post.title, 'body':post.body,'contract':post.contract}
        posts.append(this_post)
    return render_template('show_entries.html', entries=posts)
    


    
@app.route('/post')
def post():
    return render_template('post.html')   
    
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
#    g.db.execute('insert into entries (title, text) values (?, ?)',
#                 [request.form['title'], request.form['text']])
#    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))



    
if __name__ == '__main__':
    app.run()
    
    
    """
    @app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        cur = g.db.execute('select username, password from users order by id desc')
        users = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
  
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
    
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
        
        
        @app.route('/add_contract', methods=['POST'])
def add_contract():
    if not session.get('logged_in'):
        abort(401)
    new_contract= Contract(request.form['title'], request.form['body'], request.form['end_date'], request.form['user_1'], request.form['user_2'])
    db.session.add(new_contract)
    db.session.commit()
    flash('New Contract was successfully posted')
    return redirect(url_for('show_contracts')) 

"""
