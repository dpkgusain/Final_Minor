# app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)  # Allow CORS for all domains (adjust as needed for production)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:manyamf@localhost/recommendations_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    recommendations = db.relationship('Recommendation', backref='user', lazy='dynamic')

# Recommendation model
class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recommendation_type = db.Column(db.String(20), nullable=False)
    recommendation_data = db.Column(db.JSON, nullable=False)

# Token verification decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['id']).first()
            if not current_user:
                raise ValueError("User not found")
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
            return jsonify({'error': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Register user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({'error': 'User already exists!'}), 409

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'}), 201

# Login user
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials!'}), 401

    token = jwt.encode({
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token})

# Create a recommendation
@app.route('/recommendations', methods=['POST'])
@token_required
def create_recommendation(current_user):
    data = request.get_json()
    new_recommendation = Recommendation(
        user_id=current_user.id,
        recommendation_type=data['recommendation_type'],
        recommendation_data=data['recommendation_data']
    )
    db.session.add(new_recommendation)
    db.session.commit()
    return jsonify({'message': 'New recommendation created!'}), 201

# Fetch recommendations
@app.route('/recommendations', methods=['GET'])
@token_required
def get_recommendations(current_user):
    recommendations = Recommendation.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': rec.id,
        'type': rec.recommendation_type,
        'data': rec.recommendation_data
    } for rec in recommendations])

if __name__ == '__main__':
    app.run(debug=True)
