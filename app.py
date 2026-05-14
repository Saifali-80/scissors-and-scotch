from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELS ---
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.String(20), default=datetime.now().strftime("%Y-%m-%d %H:%M"))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.String(20), default=datetime.now().strftime("%Y-%m-%d"))


#14 APR ko Sign In / Create Account ko add kara tha


# Add this after Review model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # In production, use password hashing!
    created_at = db.Column(db.String(20), default=datetime.now().strftime("%Y-%m-%d"))

# Add these routes after existing routes
@app.route('/signup', methods=['POST'])
def signup():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not fullname or not email or not password:
        flash('Please fill all fields', 'error')
        return redirect(url_for('index'))
    
    # Check if user exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email already registered!', 'error')
        return redirect(url_for('index'))
    
    new_user = User(fullname=fullname, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    flash('🎉 Account created successfully! Please sign in.', 'success')
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        flash(f'✨ Welcome back, {user.fullname}!', 'success')
        return redirect(url_for('index'))
    else:
        flash('❌ Invalid email or password', 'error')
        return redirect(url_for('index'))


#14 APR ko Sign In / Create Account ko add kara tha


# Create tables
with app.app_context():
    db.create_all()

# --- ROUTES ---
@app.route('/')
def index():
    reviews = Review.query.order_by(Review.id.desc()).limit(6).all()
    return render_template('index.html', reviews=reviews)

@app.route('/book', methods=['POST'])
def book():
    name = request.form.get('name')
    phone = request.form.get('phone')
    date = request.form.get('date')
    service = request.form.get('service')
    
    if not name or not phone or not date or not service:
        flash('Please fill all fields', 'error')
        return redirect(url_for('index'))
    
    new_booking = Booking(name=name, phone=phone, date=date, service=service)
    db.session.add(new_booking)
    db.session.commit()
    flash('✅ Booking confirmed! We will contact you soon.', 'success')
    return redirect(url_for('index'))

@app.route('/submit-review', methods=['POST'])
def submit_review():
    name = request.form.get('review_name')
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    
    if not name or not rating or not comment:
        flash('Please fill all fields', 'error')
        return redirect(url_for('index'))
    
    new_review = Review(name=name, rating=int(rating), comment=comment)
    db.session.add(new_review)
    db.session.commit()
    flash('Thank you for your review!', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    bookings = Booking.query.all()
    reviews = Review.query.all()
    return render_template('admin.html', bookings=bookings, reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True, port=5001)