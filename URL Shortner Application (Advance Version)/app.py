import string, random
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Link

app = Flask(__name__)
app.config['SECRET_KEY'] = 'advanced-secret-key-99'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        
        if len(user) < 5 or len(user) > 9:
            flash("Username must be between 5 to 9 characters long", "danger")
        elif User.query.filter_by(username=user).first():
            flash("This username already exists...", "danger")
        else:
            new_user = User(username=user, password=generate_password_hash(pwd))
            db.session.add(new_user)
            db.session.commit()
            flash("Signup successful! Please login.", "success")
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Invalid username or password", "danger")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_links = Link.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', links=user_links)

@app.route('/shorten', methods=['POST'])
@login_required
def shorten():
    original = request.form.get('url')
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    new_link = Link(original_url=original, short_code=code, user_id=current_user.id)
    db.session.add(new_link)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/<short_code>')
def redirect_to_url(short_code):
    link = Link.query.filter_by(short_code=short_code).first_or_404()
    return redirect(link.original_url)

if __name__ == '__main__':
    app.run(debug=True)