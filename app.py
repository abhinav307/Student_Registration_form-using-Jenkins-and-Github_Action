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

from flask import Flask, request, jsonify, send_from_directory, g

app = Flask(__name__)
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
# CORS – add headers to every response
# ---------------------------------------------------------------------------

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


# ---------------------------------------------------------------------------
# Page routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Serve index.html from the project root directory."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(root_dir, "index.html")


@app.route("/dashboard")
def dashboard():
    """Serve the dashboard page from the templates folder."""
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    return send_from_directory(templates_dir, "dashboard.html")


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
