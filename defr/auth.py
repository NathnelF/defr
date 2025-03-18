from .tables import db, User
import functools
from flask import(Blueprint, flash, g, redirect, render_template, request, session, url_for)

from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods = (['GET', 'POST']))
def register():
    if request.method == 'POST':    
        email = request.form['email']
        password = request.form['password']
        error = None

        if not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                new_user = User(email = email, password = generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()
            except db.IntegrityError:
                error = f"User {email} is already registered"
            else:
                return redirect(url_for("auth.login"))
            
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods = (['GET', 'POST']))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        user = User.query.filter_by(email=email).first()

        if user is None:
            error = "Incorrect Email."
        elif not check_password_hash(user.password, password):
            error = "Incorrect Password."

        if error is None:
            session.clear()
            session['user_id'] = user.user_id
            return redirect(url_for('contracts.index'))
        
        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(user_id=user_id).first()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view