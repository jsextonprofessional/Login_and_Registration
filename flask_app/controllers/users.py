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
    if User.registration_validation(request.form):
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        user = User.insert_user(data)
        session['user_id'] = user
        session['first_name'] = request.form['first_name']
        return redirect('/success')
    return redirect('/')

@app.route('/users/login', methods=['POST'])
def user_login():
    users = User.select_users_by_email(request.form)
    if len(users) != 1:
        flash('Account associated with that email address does not exist.')
        return redirect('/')
    user = users[0]
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Incorrect password.')
        return redirect('/')
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    return redirect('/success')

@app.route('/success')
def successful_login_page():
    if 'user_id' not in session:
        flash('Must log in to view this page.')
        return redirect('/')
    return render_template('success.html')

@app.route('/logout')
def user_logout():
    session.clear()
    return redirect('/')