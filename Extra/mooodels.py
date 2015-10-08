# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

from . import db

# Models
class User(db.Model): # Inherit Model from sqlalchemy
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=False)
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    def __repr__(self):
        return '<User %r>' % self.username
        
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'))
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.Column(db.String(20))#db.relationship('User',
        #backref=db.backref('submissions', lazy='dynamic'))

    def __init__(self, title, body, contract_id, user, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.contract_id = contract_id
        self.user = user

    def __repr__(self):
        return '<Submission %r>' % self.title
        
class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.Text)
    end_date = db.Column(db.String(10))
    user_1 = db.Column(db.String(50))
    user_2 = db.Column(db.String(50))
    start_date = db.Column(db.DateTime)
    submissions = db.relationship('Submission', backref='Contract', lazy='dynamic')
    def __init__(self, title, body, end_date, user_1, user_2, user_3=None, start_date=None):
        if start_date is None:
            start_date = datetime.utcnow()
        self.start_date = start_date
        self.end_date = end_date    
        self.title = title
        self.body = body
        self.user_1 = user_1
        self.user_2 = user_2
        self.user_3 = user_3
    def __repr__(self):
        return '<Contract %r>' % self.title
        #user_1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
     #db.relationship('User', backref=db.backref('contracts', lazy='dynamic'))
    #user_3_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #user_3 = db.relationship('User', backref=db.backref('contracts', lazy='dynamic'))
    #db.relationship('User', backref=db.backref('contracts', lazy='dynamic'))
    #user_2_id = db.Column(db.Integer, db.ForeignKey('user.id'))
# Routes
