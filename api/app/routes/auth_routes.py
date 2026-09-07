from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from app.services.auth_service import (
    create_user,
    authenticate_user,
    get_user_by_id,
    update_user_profile,
    update_user_password
)


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}

    # Gets the data sent by the client.
    # strip() removes spaces at the beginning and end.
    # lower() normalizes the email to lowercase letters.
    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # Dictionary where errors for each field will be stored.
    errors = {}

    # Username validation
    if not username:
        errors["username"] = "Username is required."
    elif len(username) < 3:
        errors["username"] = "Username must be at least 3 characters."

    # Email validation
    if not email:
        errors["email"] = "Email is required."
    elif "@" not in email:
        errors["email"] = "Invalid email address."

    # Password validation
    if not password:
        errors["password"] = "Password is required."
    elif len(password) < 6:
        errors["password"] = "Password must be at least 6 characters."

    # If there are any errors, it does not proceed to the service.
    if errors:
        return jsonify({
            "success": False,
            "message": "Validation failed.",
            "errors": errors
        }), 400

    try:
        user = create_user(
            username=username,
            email=email,
            password=password
        )

        access_token = create_access_token(
            identity=str(user.id)
        )

        return jsonify({
            "success": True,
            "access_token": access_token,
            "message": "User registered successfully.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }), 201

    except ValueError as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 400


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}

    # Gets and normalizes the sent data.
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    errors = {}

    # Login requires an email.
    if not email:
        errors["email"] = "Email is required."
    elif "@" not in email:
        errors["email"] = "Invalid email address."

    # Password is also required.
    if not password:
        errors["password"] = "Password is required."

    # Returns all errors found before querying the database.
    if errors:
        return jsonify({
            "success": False,
            "message": "Validation failed.",
            "errors": errors
        }), 400

    try:
        user = authenticate_user(
            email=email,
            password=password
        )

        access_token = create_access_token(
            identity=str(user.id)
        )

        return jsonify({
            "success": True,
            "message": "Login successful.",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }), 200

    except ValueError as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 401


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()

    if not user_id:
        return jsonify({
            "success": False,
            "message": "Invalid user identity."
        }), 401

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Invalid user ID."
        }), 401

    user = get_user_by_id(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404

    return jsonify({
        "success": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active
        }
    }), 200


@auth_bp.put("/me")
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Invalid user ID."
        }), 401

    user = get_user_by_id(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404

    data = request.get_json(silent=True) or {}

    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()

    errors = {}

    # Profile username validation.
    if not username:
        errors["username"] = "Username is required."
    elif len(username) < 3:
        errors["username"] = "Username must be at least 3 characters."

    # Profile email validation.
    if not email:
        errors["email"] = "Email is required."
    elif "@" not in email:
        errors["email"] = "Invalid email address."

    # Prevents invalid data from reaching the service.
    if errors:
        return jsonify({
            "success": False,
            "message": "Validation failed.",
            "errors": errors
        }), 400

    try:
        user = update_user_profile(
            user=user,
            username=username,
            email=email
        )

        return jsonify({
            "success": True,
            "message": "Profile updated successfully.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active
            }
        }), 200

    except ValueError as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 400


@auth_bp.put("/me/password")
@jwt_required()
def update_password():
    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Invalid user ID."
        }), 401

    user = get_user_by_id(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404

    data = request.get_json(silent=True) or {}

    current_password = data.get("current_password", "")
    new_password = data.get("new_password", "")

    errors = {}

    # The current password is required to confirm the change.
    if not current_password:
        errors["current_password"] = "Current password is required."

    # The new password is also required.
    if not new_password:
        errors["new_password"] = "New password is required."
    elif len(new_password) < 6:
        errors["new_password"] = (
            "New password must be at least 6 characters."
        )

    # Returns errors before calling the service.
    if errors:
        return jsonify({
            "success": False,
            "message": "Validation failed.",
            "errors": errors
        }), 400

    try:
        update_user_password(
            user=user,
            current_password=current_password,
            new_password=new_password
        )

        return jsonify({
            "success": True,
            "message": "Password updated successfully."
        }), 200

    except ValueError as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 400
