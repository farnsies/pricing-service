__author__ = 'mrf'

import functools
from typing import Callable
from flask import session, flash, redirect, url_for, current_app


def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('email'):
            flash('You need to be signed in to access that page', 'danger')
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)
    return decorated_function


def requires_admin(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('email') != current_app.config.get('ADMIN', ''):
            flash("Sorry, you need administrator access for that page. And trust us--you don't want that job...", 'danger')
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)
    return decorated_function
