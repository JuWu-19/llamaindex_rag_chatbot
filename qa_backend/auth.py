from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    from app import db
    from models import User  # Import the User model
    data = request.get_json()  # Get data from the request
    username = data.get('username')
    account_number = data.get('account_number')
    password = data.get('password')
    repeat_password = data.get('repeat_password')

    if password != repeat_password:
        return jsonify({"error": "Passwords do not match"}), 400

    # Check if username or account number already exists
    if User.query.filter_by(user_name=username).first():
        return jsonify({"error": "Username already used"}), 400

    if User.query.filter_by(account_number=account_number).first():
        return jsonify({"error": "Account number already used"}), 400

    # Create new user
    hashed_password = generate_password_hash(password)
    new_user = User(user_name=username, account_number=account_number, user_password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful"}), 201

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     from app import db
#     from models import User  # Import the User model
#     data = request.get_json()
#     account_number = data.get('account_number')
#     password = data.get('password')

#     user = User.query.filter_by(account_number=account_number).first()
#     if user and check_password_hash(user.user_password, password):
#         login_user(user)  # Assuming User loader and user class are properly set up
#         return jsonify({"message": "Login successful"}), 200

#     return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    password = data.get('password')
  #  admin_password = os.getenv('ADMIN_PASSWORD', '321')
    if password == os.getenv('ADMIN_PASSWORD'):

        # Admin login simulation, typically you'd have a more complex setup
        return jsonify({"message": "Admin login successful"}), 200

    return jsonify({"error": "Invalid admin password"}), 401

    # Using a default value to check functionality
    