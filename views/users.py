__author__ = 'mrf'

from flask import Blueprint, request, session, url_for, render_template, redirect, flash
from models.user import User, errors


user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            User.register_user(email, password)
            session['email'] = email
        except errors.UserError as e:
            return e.message

        return redirect(url_for('alerts.index'))

    return render_template('users/register.html')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
        except errors.UserError as e:
            flash("Greetings! You must be new here. Please create an account.", "info")
            return redirect(url_for('users.register_user'))

        return redirect(url_for('alerts.index'))
    return render_template('users/login.html')


@user_blueprint.route('/logout')
def logout():
    session['email'] = None
    return redirect(url_for('.login_user'))
