"""
ScholarTrack - Database Manager

Responsibilities:
1. Primary: Establish MySQL connections via PyMySQL using config.py settings.
2. Resilient Fallback: If MySQL credentials fail (e.g. placeholder password in .env)
   or MySQL is unreachable, seamlessly fall back to local SQLite database so
   user registration, login, and application tracking work immediately.
3. Parameterized SQL execution & transaction management.
4. Safe connection pooling and cleanup.
"""

import os
import sqlite3
import logging
from pathlib import Path

import pymysql
from pymysql.cursors import DictCursor

from config import DatabaseConfig

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
SQLITE_DB_PATH = BASE_DIR / "scholartrack_local.db"

_USE_SQLITE = False


def _init_sqlite_schema(conn):
    """Ensure SQLite fallback tables match the ScholarTrack schema."""
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'student',
        is_active INTEGER NOT NULL DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS student_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        phone TEXT,
        date_of_birth DATE,
        gender TEXT,
        state TEXT,
        district TEXT,
        education_level TEXT,
        institution TEXT,
        course TEXT,
        specialization TEXT,
        study_year TEXT,
        marks_percentage REAL,
        annual_family_income REAL,
        category TEXT,
        preferred_categories TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS scholarship_sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_name TEXT NOT NULL,
        source_url TEXT NOT NULL UNIQUE,
        source_type TEXT NOT NULL DEFAULT 'other',
        is_approved INTEGER NOT NULL DEFAULT 0,
        is_active INTEGER NOT NULL DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS scholarships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER,
        external_id TEXT,
        title TEXT NOT NULL,
        provider TEXT NOT NULL,
        description TEXT,
        scholarship_type TEXT,
        education_level TEXT,
        eligible_courses TEXT,
        minimum_marks REAL,
        maximum_family_income REAL,
        amount_min REAL,
        amount_max REAL,
        currency TEXT NOT NULL DEFAULT 'INR',
        deadline DATE,
        official_url TEXT NOT NULL,
        is_active INTEGER NOT NULL DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (source_id) REFERENCES scholarship_sources(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS saved_scholarships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        scholarship_id INTEGER NOT NULL,
        saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (user_id, scholarship_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (scholarship_id) REFERENCES scholarships(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        scholarship_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'interested',
        application_reference TEXT,
        applied_at DATETIME,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (user_id, scholarship_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    conn.commit()


def get_db_connection():
    """
    Return active database connection (MySQL if available, or SQLite fallback).
    """
    global _USE_SQLITE

    if not _USE_SQLITE:
        try:
            settings = DatabaseConfig.get_connection_settings()
            connection = pymysql.connect(
                **settings,
                cursorclass=DictCursor
            )
            return connection
        except Exception as err:
            logger.warning(
                "MySQL connection failed (%s). Activating local fallback database.",
                err
            )
            _USE_SQLITE = True

    conn = sqlite3.connect(str(SQLITE_DB_PATH))
    conn.row_factory = sqlite3.Row
    _init_sqlite_schema(conn)
    return conn


def execute_query(query, params=None):
    """
    Execute INSERT, UPDATE, or DELETE query.
    """
    connection = get_db_connection()
    is_sqlite = isinstance(connection, sqlite3.Connection)

    try:
        sql = query
        p = params or ()

        if is_sqlite:
            # Adapt MySQL syntax for SQLite
            sql = sql.replace("%s", "?")
            sql = sql.replace("INSERT IGNORE INTO", "INSERT OR IGNORE INTO")
            cursor = connection.cursor()
            cursor.execute(sql, p)
            affected = cursor.rowcount
        else:
            with connection.cursor() as cursor:
                cursor.execute(sql, p)
                affected = cursor.rowcount

        connection.commit()
        return affected

    except Exception:
        connection.rollback()
        logger.exception("Database write operation failed.")
        raise
    finally:
        connection.close()


def fetch_one(query, params=None):
    """
    Execute SELECT query and return one dict record.
    """
    connection = get_db_connection()
    is_sqlite = isinstance(connection, sqlite3.Connection)

    try:
        sql = query
        p = params or ()

        if is_sqlite:
            sql = sql.replace("%s", "?")
            cursor = connection.cursor()
            cursor.execute(sql, p)
            row = cursor.fetchone()
            return dict(row) if row else None
        else:
            with connection.cursor() as cursor:
                cursor.execute(sql, p)
                row = cursor.fetchone()
                return row

    except Exception:
        logger.exception("Database fetch_one failed.")
        raise
    finally:
        connection.close()


def fetch_all(query, params=None):
    """
    Execute SELECT query and return list of dict records.
    """
    connection = get_db_connection()
    is_sqlite = isinstance(connection, sqlite3.Connection)

    try:
        sql = query
        p = params or ()

        if is_sqlite:
            sql = sql.replace("%s", "?")
            cursor = connection.cursor()
            cursor.execute(sql, p)
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        else:
            with connection.cursor() as cursor:
                cursor.execute(sql, p)
                rows = cursor.fetchall()
                return rows

    except Exception:
        logger.exception("Database fetch_all failed.")
        raise
    finally:
        connection.close()
