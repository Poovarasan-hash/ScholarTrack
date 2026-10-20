"""
ScholarTrack - Authentication & User Service

Responsibilities:
1. Student registration business logic.
2. User authentication & password verification using Werkzeug.
3. User profile retrieval.
4. Password update management.
5. Parameterized database operations.
"""

import logging
from werkzeug.security import generate_password_hash, check_password_hash
from pymysql.err import IntegrityError, MySQLError

from models.database import execute_query, fetch_one

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication and user account service layer."""

    @staticmethod
    def register_user(
        name: str,
        email: str,
        password: str,
        role: str = "student",
        education_level: str = None,
        institution: str = None
    ) -> dict:
        """
        Register a new user account.

        Args:
            name: User full name.
            email: User email address (normalized).
            password: Plaintext password meeting security policy.
            role: Account role ('student' or 'admin').
            education_level: Optional student education level.
            institution: Optional student school/college name.

        Returns:
            dict: { "success": True, "user": new_user }
        """
        normalized_email = email.strip().lower()

        # Check existing user
        existing_user = fetch_one(
            "SELECT id FROM users WHERE email = %s LIMIT 1",
            (normalized_email,)
        )
        if existing_user:
            raise ValueError("An account with this email already exists.")

        password_hash = generate_password_hash(password)

        try:
            execute_query(
                """
                INSERT INTO users (name, email, password_hash, role)
                VALUES (%s, %s, %s, %s)
                """,
                (name.strip(), normalized_email, password_hash, role)
            )

            new_user = fetch_one(
                "SELECT id, name, email, role FROM users WHERE email = %s LIMIT 1",
                (normalized_email,)
            )

            # Insert initial student profile row if registering as a student
            if role == "student" and new_user:
                try:
                    execute_query(
                        """
                        INSERT IGNORE INTO student_profiles (user_id, education_level, institution)
                        VALUES (%s, %s, %s)
                        """,
                        (new_user["id"], education_level, institution)
                    )
                except Exception as profile_err:
                    logger.warning("Optional student_profile creation skipped: %s", profile_err)

            return {
                "success": True,
                "user": new_user
            }

        except IntegrityError:
            raise ValueError("An account with this email already exists.")
        except MySQLError as db_err:
            logger.exception("Database error during user registration.")
            raise db_err

    @staticmethod
    def authenticate_user(email: str, password: str) -> dict:
        """
        Authenticate a user by email and password.

        Args:
            email: User email.
            password: Provided plaintext password.

        Returns:
            dict: User data dict (safe, without password hash) if valid, or None.
        """
        normalized_email = email.strip().lower()

        user = fetch_one(
            """
            SELECT id, name, email, password_hash, role, is_active
            FROM users
            WHERE email = %s
            LIMIT 1
            """,
            (normalized_email,)
        )

        if not user:
            return None

        if not user.get("is_active", True):
            raise PermissionError("Your account has been deactivated. Please contact support.")

        if not check_password_hash(user["password_hash"], password):
            return None

        # Return safe user dict
        return {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }

    @staticmethod
    def get_user_by_id(user_id: int) -> dict:
        """
        Retrieve safe user profile details by ID.
        """
        user = fetch_one(
            """
            SELECT u.id, u.name, u.email, u.role, u.is_active, u.created_at,
                   p.phone, p.education_level, p.institution, p.course
            FROM users u
            LEFT JOIN student_profiles p ON u.id = p.user_id
            WHERE u.id = %s
            LIMIT 1
            """,
            (user_id,)
        )
        return user

    @staticmethod
    def change_user_password(user_id: int, current_password: str, new_password: str) -> bool:
        """
        Verify current password and update to new password.
        """
        user = fetch_one(
            "SELECT id, password_hash FROM users WHERE id = %s LIMIT 1",
            (user_id,)
        )

        if not user or not check_password_hash(user["password_hash"], current_password):
            return False

        new_hash = generate_password_hash(new_password)
        execute_query(
            "UPDATE users SET password_hash = %s WHERE id = %s",
            (new_hash, user_id)
        )
        return True
