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

    @classmethod
    def select_users_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
# MAY NEED TO CHANGE lnr_users_schema to lnr_users_model, brb
        results = connectToMySQL('lnr_users_schema').query_db(query, data)

        users = []

        for item in results:
            users.append(User(item))

        return users

    @classmethod
    def insert_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"

        result = connectToMySQL('lnr_users_schema').query_db(query, data)

        return result

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
            flash('Email address invalid, please try again.')
            is_valid = False
    # pw - at least 8 - 255 char, was submitted
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters.')
            is_valid = False
    # confirm pw - matches pw
        if data['password'] != data['confirm_password']:
            flash('Passwords must match.')
            is_valid = False

        if len(User.select_users_by_email({'email': data['email']})) != 0:
            flash('Email address already in use.')
            is_valid = False

        return is_valid