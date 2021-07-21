import re
from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users/register', methods = ['POST'])
def user_registration():
    print(User.registration_validation(request.form))
    return redirect('/')

@app.route('/success')
def successful_login_page():
    return render_template('success.html')