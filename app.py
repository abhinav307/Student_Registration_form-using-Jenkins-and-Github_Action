"""
Flask Student Registration Application
=======================================
Provides REST API endpoints for student registration and management,
backed by an SQLite database.
"""

import os
import re
import sqlite3
from datetime import datetime
from functools import wraps

from flask import Flask, request, jsonify, send_from_directory, g, session, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super-secret-key"
app.config["DATABASE"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.db")


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def get_db():
    """Open a new database connection if there is none yet for the current
    application context and return it."""
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL")
    return g.db


@app.teardown_appcontext
def close_db(exception):
    """Close the database connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(db_path=None):
    """Create the students table if it does not already exist."""
    if db_path:
        app.config["DATABASE"] = db_path
    with app.app_context():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name      TEXT    NOT NULL,
                last_name       TEXT    NOT NULL,
                email           TEXT    NOT NULL UNIQUE,
                phone           TEXT    NOT NULL,
                dob             TEXT    NOT NULL,
                gender          TEXT    NOT NULL,
                course          TEXT    NOT NULL,
                semester        TEXT    NOT NULL,
                roll_number     TEXT,
                enroll_year     TEXT,
                address         TEXT,
                registered_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                email           TEXT    NOT NULL UNIQUE,
                password_hash   TEXT    NOT NULL,
                full_name       TEXT,
                bio             TEXT,
                theme           TEXT    DEFAULT 'light',
                avatar_url      TEXT    DEFAULT 'https://ui-avatars.com/api/?name=User&background=random',
                cover_url       TEXT    DEFAULT 'https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=1000&q=80',
                twitter         TEXT,
                linkedin        TEXT,
                github          TEXT,
                notifications   INTEGER DEFAULT 1
            )
            """
        )
        
        # Safely add columns if they don't exist (for existing dev DBs)
        try:
            db.execute("ALTER TABLE users ADD COLUMN avatar_url TEXT DEFAULT 'https://ui-avatars.com/api/?name=User&background=random'")
            db.execute("ALTER TABLE users ADD COLUMN cover_url TEXT DEFAULT 'https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=1000&q=80'")
            db.execute("ALTER TABLE users ADD COLUMN twitter TEXT")
            db.execute("ALTER TABLE users ADD COLUMN linkedin TEXT")
            db.execute("ALTER TABLE users ADD COLUMN github TEXT")
            db.execute("ALTER TABLE users ADD COLUMN notifications INTEGER DEFAULT 1")
            db.execute("ALTER TABLE users ADD COLUMN marketing_emails INTEGER DEFAULT 1")
        except sqlite3.OperationalError:
            pass # Columns already exist

        db.commit()


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

EMAIL_RE = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
PHONE_RE = re.compile(r"^\d{10}$")


def normalize_student_data(data):
    """Convert camelCase keys from frontend to snake_case for the database."""
    mapping = {
        'firstName': 'first_name',
        'lastName': 'last_name',
        'rollNumber': 'roll_number',
        'enrollYear': 'enroll_year',
    }
    normalized = {}
    for key, value in data.items():
        new_key = mapping.get(key, key)
        normalized[new_key] = value
    return normalized


def validate_student(data):
    """Return a list of error strings for the given student data dict."""
    errors = []

    required_fields = [
        "first_name", "last_name", "email", "phone",
        "dob", "gender", "course", "semester",
    ]
    for field in required_fields:
        value = data.get(field)
        if not value or (isinstance(value, str) and not value.strip()):
            errors.append(f"{field} is required.")

    # Email format
    email = data.get("email", "")
    if email and not EMAIL_RE.match(email.strip()):
        errors.append("Email must be a valid email address.")

    # Phone – exactly 10 digits
    phone = data.get("phone", "")
    if phone and not PHONE_RE.match(phone.strip()):
        errors.append("Phone must be exactly 10 digits.")

    return errors


def row_to_dict(row):
    """Convert a sqlite3.Row to a plain dictionary."""
    return dict(row) if row else None


# ---------------------------------------------------------------------------
# Auth helpers & Context
# ---------------------------------------------------------------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_user():
    user = None
    if 'user_id' in session:
        db = get_db()
        user_row = db.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],)).fetchone()
        if user_row:
            user = row_to_dict(user_row)
    return dict(current_user=user)


# ---------------------------------------------------------------------------
# CORS – add headers to every response
# ---------------------------------------------------------------------------

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


# ---------------------------------------------------------------------------
# Page & Auth routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Render index.html from templates."""
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    """Render the dashboard page."""
    return render_template("dashboard.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        db = get_db()
        user_row = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user_row and check_password_hash(user_row["password_hash"], password):
            session['user_id'] = user_row['id']
            return redirect(url_for('dashboard'))
        return render_template("login.html", error="Invalid email or password.")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        full_name = request.form.get("full_name")
        
        db = get_db()
        try:
            db.execute("INSERT INTO users (email, password_hash, full_name) VALUES (?, ?, ?)",
                       (email, generate_password_hash(password), full_name))
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template("signup.html", error="Email already registered.")
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        bio = request.form.get("bio")
        avatar_url = request.form.get("avatar_url")
        cover_url = request.form.get("cover_url")
        twitter = request.form.get("twitter")
        linkedin = request.form.get("linkedin")
        github = request.form.get("github")
        db = get_db()
        db.execute(
            "UPDATE users SET full_name = ?, bio = ?, avatar_url = ?, cover_url = ?, twitter = ?, linkedin = ?, github = ? WHERE id = ?", 
            (full_name, bio, avatar_url, cover_url, twitter, linkedin, github, session['user_id'])
        )
        db.commit()
        return redirect(url_for('profile'))
    return render_template("profile.html")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        theme = request.form.get("theme")
        password = request.form.get("password")
        notifications = request.form.get("notifications")
        marketing_emails = request.form.get("marketing_emails")
        
        notif_val = 1 if notifications == 'on' else 0
        mkt_val = 1 if marketing_emails == 'on' else 0
        
        db = get_db()
        if theme:
            db.execute("UPDATE users SET theme = ?, notifications = ?, marketing_emails = ? WHERE id = ?", (theme, notif_val, mkt_val, session['user_id']))
        if password:
            db.execute("UPDATE users SET password_hash = ? WHERE id = ?", (generate_password_hash(password), session['user_id']))
        db.commit()
        return redirect(url_for('settings'))
    return render_template("settings.html")


# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------

@app.route("/api/register", methods=["POST"])
def register_student():
    """Register a new student. Accepts JSON, validates, and persists to DB."""
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"success": False, "message": "Invalid or missing JSON body."}), 400

        # Normalize camelCase keys from frontend to snake_case
        data = normalize_student_data(data)

        errors = validate_student(data)
        if errors:
            return jsonify({"success": False, "message": "Validation failed.", "errors": errors}), 400

        db = get_db()
        db.execute(
            """
            INSERT INTO students
                (first_name, last_name, email, phone, dob, gender,
                 course, semester, roll_number, enroll_year, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["first_name"].strip(),
                data["last_name"].strip(),
                data["email"].strip(),
                data["phone"].strip(),
                data["dob"].strip(),
                data["gender"].strip(),
                data["course"].strip(),
                data["semester"].strip(),
                data.get("roll_number", "").strip() if data.get("roll_number") else None,
                data.get("enroll_year", "").strip() if data.get("enroll_year") else None,
                data.get("address", "").strip() if data.get("address") else None,
            ),
        )
        db.commit()

        return jsonify({
            "success": True,
            "message": "Student registered successfully.",
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "success": False,
            "message": "A student with this email already exists.",
        }), 409
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": f"An unexpected error occurred: {str(exc)}",
        }), 500


@app.route("/api/students", methods=["GET"])
def get_students():
    """Return all students as JSON. Supports ?search= query parameter to
    filter by first_name, last_name, email, or course."""
    try:
        db = get_db()
        search = request.args.get("search", "").strip()

        if search:
            like = f"%{search}%"
            rows = db.execute(
                """
                SELECT * FROM students
                WHERE first_name LIKE ? OR last_name LIKE ?
                   OR email LIKE ? OR course LIKE ?
                ORDER BY id DESC
                """,
                (like, like, like, like),
            ).fetchall()
        else:
            rows = db.execute("SELECT * FROM students ORDER BY id DESC").fetchall()

        students = [row_to_dict(r) for r in rows]
        return jsonify({"success": True, "students": students, "count": len(students)}), 200

    except Exception as exc:
        return jsonify({
            "success": False,
            "message": f"An unexpected error occurred: {str(exc)}",
        }), 500


@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    """Return a single student by ID."""
    try:
        db = get_db()
        row = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()

        if not row:
            return jsonify({"success": False, "message": "Student not found."}), 404

        return jsonify({"success": True, "student": row_to_dict(row)}), 200

    except Exception as exc:
        return jsonify({
            "success": False,
            "message": f"An unexpected error occurred: {str(exc)}",
        }), 500


@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """Delete a student by ID."""
    try:
        db = get_db()
        row = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()

        if not row:
            return jsonify({"success": False, "message": "Student not found."}), 404

        db.execute("DELETE FROM students WHERE id = ?", (student_id,))
        db.commit()

        return jsonify({"success": True, "message": "Student deleted successfully."}), 200

    except Exception as exc:
        return jsonify({
            "success": False,
            "message": f"An unexpected error occurred: {str(exc)}",
        }), 500


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Return aggregate statistics: total count, course breakdown, gender breakdown."""
    try:
        db = get_db()

        # Total count
        total = db.execute("SELECT COUNT(*) AS total FROM students").fetchone()["total"]

        # Course breakdown
        course_rows = db.execute(
            "SELECT course, COUNT(*) AS count FROM students GROUP BY course ORDER BY count DESC"
        ).fetchall()
        courses = {r["course"]: r["count"] for r in course_rows}

        # Gender breakdown
        gender_rows = db.execute(
            "SELECT gender, COUNT(*) AS count FROM students GROUP BY gender ORDER BY count DESC"
        ).fetchall()
        genders = {r["gender"]: r["count"] for r in gender_rows}

        return jsonify({
            "success": True,
            "total": total,
            "courses": courses,
            "genders": genders,
        }), 200

    except Exception as exc:
        return jsonify({
            "success": False,
            "message": f"An unexpected error occurred: {str(exc)}",
        }), 500


# ---------------------------------------------------------------------------
# Application entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
