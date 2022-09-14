from cryptoTracker import app
from flask import render_template, redirect, url_for, flash, request
from cryptoTracker.models import User
from cryptoTracker.forms import RegisterForm, LoginForm
from cryptoTracker import db
from flask_login import login_user, logout_user, login_required, current_user
@app.route("/")
def home_page():

    return render_template('mainpage.html')

@app.route('/account', methods=['GET', 'POST'])  
def register_page():
    form = RegisterForm()
    if form.is_submitted():
        user_to_create = User(username=form.username.data,
        email_adress =form.email_adress.data,
        password=form.password1.data)
        db.session.add(user_to_create)  
        db.session.commit()
        login_user(user_to_create)
        flash(f'account created successfully! you are logged in as {user_to_create.username}', category='success')
        return redirect(url_for('profile_page'))
    if form.errors != {}: #if there are is errors from the validarions (it returns empty dict if no errors)
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('registerpage.html', form = form) 

@app.route('/trade')
def trade_page():
    return render_template('trades.html')

@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    form = LoginForm()
    attempted_user = User.query.filter_by(username=form.username.data).first()
    if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
        login_user(attempted_user)
        flash(f'Success! You are Logged in as: {attempted_user.username}', category='success')
        return redirect(url_for('trade_page'))
    else:
        flash('Username or Password is not correct! please try again', category='danger')
    return render_template('loginpage.html', form = form)


@app.route('/profile')
def profile_page():
    return render_template('profile.html')

@app.route('/profilesettings')
def profile_settings():
    return render_template('profileaccountsettings.html')

@app.route('/billing')
def profile_billing():
    return render_template('profilebilling.html')

@app.route('/notifications')
def profile_notification():
    return render_template('profilenotification.html')

@app.route('/security')
def profile_security():
    return render_template('profilesecurity.html')
    
@app.route('/exit')
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('home_page'))



