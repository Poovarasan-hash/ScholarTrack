"""
ScholarTrack - Authentication Controller

Features:
- Student registration
- Login
- Logout
- Current session verification (/me)
- Password change
- Session management & CSRF protection
- Input validation & HTTP responses
"""

import re
import secrets
import hmac
from functools import wraps

from flask import (
    Blueprint,
    jsonify,
    request,
    session,
    current_app
)

from services.auth_service import AuthService


# =====================================================
# 1. AUTHENTICATION BLUEPRINT
# =====================================================

auth_bp = Blueprint("auth", __name__)


# =====================================================
# 2. RESPONSE HELPERS
# =====================================================

def success_response(message, data=None, status_code=200):
    response = {
        "success": True,
        "message": message
    }

    if data is not None:
        response["data"] = data

    return jsonify(response), status_code


def error_response(message, status_code=400):
    return jsonify({
        "success": False,
        "error": message,
        "message": message
    }), status_code


# =====================================================
# 3. REQUEST VALIDATION
# =====================================================

def get_json_body():
    if not request.is_json:
        return None

    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return None

    return body


def validate_email(email):
    if not isinstance(email, str):
        return False

    email = email.strip()
    if len(email) > 254:
        return False

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.fullmatch(pattern, email))


def validate_password(password):
    """
    Password policy:
    - At least 8 characters
    - Maximum 128 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """
    if not isinstance(password, str):
        return False

    if not 8 <= len(password) <= 128:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    return True


# =====================================================
# 4. SESSION AUTHENTICATION DECORATOR
# =====================================================

def login_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return error_response(
                "Please log in to access this resource.",
                401
            )
        return view_function(*args, **kwargs)

    return wrapper


# =====================================================
# 5. STUDENT REGISTRATION
# =====================================================

@auth_bp.route("/register", methods=["POST"])
def register():
    body = get_json_body()

    if body is None:
        return error_response(
            "A valid JSON request body is required.",
            400
        )

    name = body.get("name") or body.get("full_name")
    email = body.get("email")
    password = body.get("password")
    confirm_password = body.get("confirm_password") or password
    education_level = body.get("education_level")
    institution = body.get("institution")

    if not name or not email or not password:
        return error_response(
            "Name, email, and password are required.",
            400
        )

    name = name.strip()
    email = email.strip().lower()

    if not 2 <= len(name) <= 100:
        return error_response(
            "Name must contain between 2 and 100 characters.",
            400
        )

    if not validate_email(email):
        return error_response(
            "Enter a valid email address.",
            400
        )

    if not validate_password(password):
        return error_response(
            "Password must contain 8–128 characters, "
            "including uppercase, lowercase, and a number.",
            400
        )

    if password != confirm_password:
        return error_response(
            "Passwords do not match.",
            400
        )

    try:
        AuthService.register_user(
            name=name,
            email=email,
            password=password,
            role="student",
            education_level=education_level,
            institution=institution
        )
        return success_response(
            "Registration successful. You can now log in.",
            status_code=201
        )
    except ValueError as err:
        return error_response(str(err), 409)
    except Exception:
        current_app.logger.exception("Unexpected error during registration.")
        return error_response(
            "Unable to complete registration. Please try again.",
            500
        )


# =====================================================
# 6. STUDENT LOGIN
# =====================================================

@auth_bp.route("/login", methods=["POST"])
def login():
    body = get_json_body()

    if body is None:
        return error_response(
            "A valid JSON request body is required.",
            400
        )

    email = body.get("email")
    password = body.get("password")

    if not isinstance(email, str) or not isinstance(password, str):
        return error_response(
            "Email and password are required.",
            400
        )

    email = email.strip().lower()

    if not validate_email(email) or len(password) > 128:
        return error_response(
            "Invalid email or password.",
            401
        )

    try:
        user = AuthService.authenticate_user(email, password)
        if not user:
            return error_response(
                "Invalid email or password.",
                401
            )

        # Clear and rotate session
        session.clear()
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["user_role"] = user["role"]

        csrf_token = secrets.token_urlsafe(32)
        session["csrf_token"] = csrf_token
        session.permanent = True

        return success_response(
            "Login successful.",
            {
                "user": user,
                "csrf_token": csrf_token,
                "redirect_url": "dashboard.html"
            }
        )
    except PermissionError as perm_err:
        return error_response(str(perm_err), 403)
    except Exception:
        current_app.logger.exception("Database error during login.")
        return error_response(
            "Unable to log in right now. Please try again.",
            500
        )


# =====================================================
# 7. CURRENT USER
# =====================================================

@auth_bp.route("/me", methods=["GET"])
@login_required
def current_user():
    try:
        user = AuthService.get_user_by_id(session["user_id"])
        if not user:
            session.clear()
            return error_response(
                "User account not found.",
                401
            )

        return success_response(
            "Current user retrieved successfully.",
            {
                "user": user,
                "csrf_token": session.get("csrf_token")
            }
        )
    except Exception:
        current_app.logger.exception("Database error retrieving current user.")
        return error_response(
            "Unable to retrieve user information.",
            500
        )


# =====================================================
# 8. LOGOUT
# =====================================================

@auth_bp.route("/logout", methods=["POST"])
def logout():
    if not session.get("user_id"):
        return success_response(
            "You are already logged out."
        )

    supplied_token = request.headers.get("X-CSRF-Token", "")
    expected_token = session.get("csrf_token", "")

    # Optional CSRF token check if present
    if supplied_token and expected_token:
        if not hmac.compare_digest(supplied_token, expected_token):
            return error_response(
                "Invalid CSRF token.",
                403
            )

    session.clear()
    return success_response(
        "Logout successful."
    )


# =====================================================
# 9. CHANGE PASSWORD
# =====================================================

@auth_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    body = get_json_body()

    if body is None:
        return error_response(
            "A valid JSON request body is required.",
            400
        )

    current_password = body.get("current_password")
    new_password = body.get("new_password")
    confirm_password = body.get("confirm_password")

    if not all(
        isinstance(value, str)
        for value in [current_password, new_password, confirm_password]
    ):
        return error_response(
            "All password fields are required.",
            400
        )

    if not validate_password(new_password):
        return error_response(
            "New password must contain at least 8 characters, "
            "including uppercase, lowercase, and a number.",
            400
        )

    if new_password != confirm_password:
        return error_response(
            "New passwords do not match.",
            400
        )

    if current_password == new_password:
        return error_response(
            "New password must differ from the current password.",
            400
        )

    try:
        success = AuthService.change_user_password(
            session["user_id"],
            current_password,
            new_password
        )

        if not success:
            return error_response(
                "Current password is incorrect.",
                401
            )

        session.clear()
        return success_response(
            "Password changed. Please log in again."
        )
    except Exception:
        current_app.logger.exception("Database error changing password.")
        return error_response(
            "Unable to change password right now.",
            500
        )
