from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from models.user import User

auth = Blueprint("auth", __name__)

# ===========================
# User Registration
# ===========================
@auth.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")

    # Validate input
    if not full_name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"message": "Email already registered"}), 400

    # Hash password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Create user
    user = User(
        full_name=full_name,
        email=email,
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registration Successful"}), 201


# ===========================
# User Login
# ===========================
@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    # Validate input
    if not email or not password:
        return jsonify({"message": "Email and Password are required"}), 400

    # Check user
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Verify password
    if bcrypt.check_password_hash(user.password, password):
        return jsonify({
            "message": "Login Successful",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role
            }
        }), 200

    return jsonify({"message": "Invalid Password"}), 401