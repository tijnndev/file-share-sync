from datetime import datetime
import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import logging
from sqlalchemy.orm import DeclarativeBase

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'apk', 'exe', 'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import User, File

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@login_required
def index():
    files = File.query.filter_by(user_id=current_user.id).all()
    return render_template('files.html', files=files)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
            
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        existing_file = File.query.filter_by(filename=filename, user_id=current_user.id).first()

        if existing_file:
            existing_file_path = os.path.join(app.config['UPLOAD_FOLDER'], existing_file.filename)
            if os.path.exists(existing_file_path):
                os.remove(existing_file_path)

            file.save(file_path)
            existing_file.uploaded_at = datetime.now()
            db.session.commit()
            flash('File successfully replaced')

        else:
            file.save(file_path)
            new_file = File(
                filename=filename,
                user_id=current_user.id,
                uploaded_at=datetime.now()
            )
            db.session.add(new_file)
            db.session.commit()
            flash('File successfully uploaded')

        return redirect(url_for('index'))

    flash('File type not allowed')
    return redirect(url_for('index'))


@app.route('/download/<filename>')
@login_required
def download_file(filename):
    file = File.query.filter_by(filename=filename, user_id=current_user.id).first()
    if file:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    flash('File not found')
    return redirect(url_for('index'))

@app.route('/delete/<int:file_id>')
@login_required
def delete_file(file_id):
    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        flash('Permission denied')
        return redirect(url_for('index'))
        
    try:
        db.session.delete(file)
        db.session.commit()
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    except Exception as e:
        flash(f'Error deleting file: {str(e)}')
    return redirect(url_for('index'))

with app.app_context():
    db.create_all()
