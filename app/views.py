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
        new_contract= Contract(request.form['body'], request.form['end_date'], request.form['user_1'], request.form['user_2'])
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
        this_contract = {"body":contract.body, "end_date":contract.end_date, 'body':contract.body,'user_1':contract.user_1,'user_2':contract.user_2, 'id':contract.id}
        contracts.append(this_contract)
    return render_template('show_contracts.html', contracts=contracts)


@app.route('/contracts/<id>')
def show_contract(id):
    contract = Contract.query.filter_by(id=id).first()
    this_contract = {'body':contract.body, 'id':contract.id, 'end_date':contract.end_date}
    return render_template('contract.html', contract=this_contract)
    
@app.route('/contract/remove/<id>', methods=['GET'])
def remove(id):
    contract = Contract.query.filter_by(id=id).first()
    db.session.remove(contract)
    flash('Contract has been deleted')
    return redirect(url_for('index'))


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    error = None
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        #c = Contract.query.get(request.form.get('contract'))
        new_submission= Submission(body=request.form.get('body'), contract_id=request.form.get('contract'), author=session.get('username'))
        db.session.add(new_submission)
        db.session.commit()
        flash('Submission complete')
        return redirect(url_for('show_submissions'))     
    else:
        error = 'Invalid entry' 
    contracts = []
    contract_query = Contract.query.all()
    for contract in contract_query:
        this_contract = {'body':contract.body, 'id':contract.id}
        contracts.append(this_contract)
    return render_template('submit.html', contracts=contracts)   
    
@app.route('/submissions')
def show_submissions():
    subs = []
    sub_query = Submission.query.all()
    for sub in sub_query:
        this_sub = {'body':sub.body, 'contract':sub.contract_id}
        subs.append(this_sub)
    return render_template('show_submissions.html', submissions=subs)
    


    
@app.route('/post')
def post():
    return render_template('post.html')   
    
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))



