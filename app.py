import os
from functools import wraps
from flask import Flask, render_template, session, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from controllers.users import create_user, get_user_by_id, get_user_by_email

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def home():
    user_id = session.get('user_id')

    return render_template('index.html', user=get_user_by_id(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)

        user_id = create_user(username, email, hashed_password)
        session['user_id'] = user_id

        return redirect('/')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = get_user_by_email(email)

        if user is None:
            return 'Invalid email or password', 401

        if not check_password_hash(
            user['password'],
            password
        ):
            return 'Invalid email or password', 401

        session['user_id'] = user['id']

        return redirect('/')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)