import re
from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

class User():
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def registration_validation(data):
        is_valid = True

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    # first name - letters only, 2-45 characters, not already in db and was submitted
        if len(data['first_name']) < 2 or len(data['first_name']) > 45:
            flash('First Name should be between 2 and 45 characters.')
    # last name - same as first name
        if len(data['last_name']) < 2 or len(data['last_name']) > 45:
            flash('Last Name should be between 2 and 45 characters.')
    # email - valid email format, not already in DB, was submitted, not already in db
        if not EMAIL_REGEX.match(data['email']):
            flash('Email address invalid, please try again')
            is_valid = False
    # pw - at least 8 - 255 char, was submitted
    # confirm pw - matches pw
        return is_valid