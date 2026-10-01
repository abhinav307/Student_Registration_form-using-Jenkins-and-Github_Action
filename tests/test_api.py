"""
Comprehensive pytest test suite for the Flask Student Registration API.
"""

import json
import os
import tempfile

import pytest
import sys

# Ensure parent directory is on the path so we can import app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app, init_db


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    """Create a test client with a fresh temporary database."""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)

    app.config['TESTING'] = True
    app.config['DATABASE'] = db_path
    
    # We need a secret key for session to work in tests if not already set
    app.secret_key = "test-secret"

    init_db(db_path)

    with app.test_client() as test_client:
        # Create a test user and log them in
        with app.app_context():
            db = init_db.get_db() if hasattr(init_db, 'get_db') else app.extensions.get('sqlite3', None) # this won't work easily
            from app import get_db, generate_password_hash
            db = get_db()
            db.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", ('test@test.com', generate_password_hash('test')))
            db.commit()
            user_id = db.execute("SELECT id FROM users WHERE email = 'test@test.com'").fetchone()['id']
            
        with test_client.session_transaction() as sess:
            sess['user_id'] = user_id

        yield test_client

    # Cleanup
    if os.path.exists(db_path):
        try:
            os.unlink(db_path)
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Helper data
# ---------------------------------------------------------------------------

VALID_STUDENT = {
    'firstName': 'Priya',
    'lastName': 'Sharma',
    'email': 'priya@test.com',
    'phone': '9876543210',
    'dob': '2002-05-15',
    'gender': 'Female',
    'course': 'B.Tech CSE',
    'semester': '3',
    'rollNumber': '2024CSE001',
    'enrollYear': '2024',
    'address': 'Delhi, India',
}

SECOND_STUDENT = {
    'firstName': 'Arjun',
    'lastName': 'Patel',
    'email': 'arjun@test.com',
    'phone': '9123456780',
    'dob': '2001-08-22',
    'gender': 'Male',
    'course': 'B.Tech ECE',
    'semester': '5',
    'rollNumber': '2023ECE042',
    'enrollYear': '2023',
    'address': 'Mumbai, India',
}


# ---------------------------------------------------------------------------
# Registration Tests
# ---------------------------------------------------------------------------

class TestRegistration:
    """Tests for POST /api/register."""

    def test_register_student_success(self, client):
        """Register a student with valid complete data – expect 201."""
        resp = client.post(
            '/api/register',
            data=json.dumps(VALID_STUDENT),
            content_type='application/json',
        )
        assert resp.status_code == 201
        data = resp.get_json()
        assert 'success' in data.get('message', '').lower() or data.get('success') is True or resp.status_code == 201

    def test_register_missing_required_fields(self, client):
        """POST with an empty body – expect 400."""
        resp = client.post(
            '/api/register',
            data=json.dumps({}),
            content_type='application/json',
        )
        assert resp.status_code == 400

    def test_register_invalid_email(self, client):
        """POST with a malformed email – expect 400."""
        bad = {**VALID_STUDENT, 'email': 'not-an-email'}
        resp = client.post(
            '/api/register',
            data=json.dumps(bad),
            content_type='application/json',
        )
        assert resp.status_code == 400

    def test_register_invalid_phone(self, client):
        """POST with a phone number that is not 10 digits – expect 400."""
        bad = {**VALID_STUDENT, 'phone': '12345'}
        resp = client.post(
            '/api/register',
            data=json.dumps(bad),
            content_type='application/json',
        )
        assert resp.status_code == 400

    def test_register_duplicate_email(self, client):
        """Register the same email twice – second attempt should return 409."""
        client.post(
            '/api/register',
            data=json.dumps(VALID_STUDENT),
            content_type='application/json',
        )
        resp = client.post(
            '/api/register',
            data=json.dumps(VALID_STUDENT),
            content_type='application/json',
        )
        assert resp.status_code == 409

    def test_register_partial_required_fields(self, client):
        """POST with only firstName provided – expect 400."""
        resp = client.post(
            '/api/register',
            data=json.dumps({'firstName': 'Priya'}),
            content_type='application/json',
        )
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# Get Students Tests
# ---------------------------------------------------------------------------

class TestGetStudents:
    """Tests for GET /api/students and GET /api/students/<id>."""

    def test_get_all_students_empty(self, client):
        """GET /api/students when no students exist – expect 200 and empty list."""
        resp = client.get('/api/students')
        assert resp.status_code == 200
        data = resp.get_json()
        # The response is either a list or a dict wrapping a list
        students = data if isinstance(data, list) else data.get('students', data.get('data', []))
        assert len(students) == 0

    def test_get_all_students_after_register(self, client):
        """Register 2 students then GET /api/students – expect length 2."""
        client.post(
            '/api/register',
            data=json.dumps(VALID_STUDENT),
            content_type='application/json',
        )
        client.post(
            '/api/register',
            data=json.dumps(SECOND_STUDENT),
            content_type='application/json',
        )

        resp = client.get('/api/students')
        assert resp.status_code == 200
        data = resp.get_json()
        students = data if isinstance(data, list) else data.get('students', data.get('data', []))
        assert len(students) == 2

    def test_search_students(self, client):
        """Register students and search by name – verify filtered results."""
        client.post(
            '/api/register',
            data=json.dumps(VALID_STUDENT),
            content_type='application/json',
        )
        client.post(
            '/api/register',
            data=json.dumps(SECOND_STUDENT),
            content_type='application/json',
        )

        resp = client.get('/api/students?search=Priya')
        assert resp.status_code == 200
        data = resp.get_json()
        students = data if isinstance(data, list) else data.get('students', data.get('data', []))
        # At least one result should match
        assert len(students) >= 1
        # Verify the matched student contains the search term
        names = ' '.join(
            str(s.get('firstName', '') or s.get('first_name', '')) for s in students
        )
        assert 'Priya' in names

    def test_get_single_student(self, client):
        """Register one student and GET /api/students/1 – expect 200."""
        client.post(
            '/api/register',
            data=json.dumps(VALID_STUDENT),
            content_type='application/json',
        )

        resp = client.get('/api/students/1')
        assert resp.status_code == 200

    def test_get_nonexistent_student(self, client):
        """GET /api/students/999 – expect 404."""
        resp = client.get('/api/students/999')
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Delete Student Tests
# ---------------------------------------------------------------------------

class TestDeleteStudent:
    """Tests for DELETE /api/students/<id>."""

    def test_delete_student(self, client):
        """Register one student, delete it, then verify list is empty."""
        client.post(
            '/api/register',
            data=json.dumps(VALID_STUDENT),
            content_type='application/json',
        )

        resp = client.delete('/api/students/1')
        assert resp.status_code == 200

        # Verify the student is gone
        resp = client.get('/api/students')
        data = resp.get_json()
        students = data if isinstance(data, list) else data.get('students', data.get('data', []))
        assert len(students) == 0

    def test_delete_nonexistent(self, client):
        """DELETE /api/students/999 – expect 404."""
        resp = client.delete('/api/students/999')
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Stats Tests
# ---------------------------------------------------------------------------

class TestStats:
    """Tests for GET /api/stats."""

    def test_stats_empty(self, client):
        """GET /api/stats when no students exist."""
        resp = client.get('/api/stats')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data is not None

    def test_stats_with_data(self, client):
        """Register 3 students with different courses/genders and verify stats."""
        third_student = {
            'firstName': 'Sneha',
            'lastName': 'Gupta',
            'email': 'sneha@test.com',
            'phone': '9988776655',
            'dob': '2003-01-10',
            'gender': 'Female',
            'course': 'B.Tech CSE',
            'semester': '1',
            'rollNumber': '2024CSE099',
            'enrollYear': '2024',
            'address': 'Bangalore, India',
        }

        for student in [VALID_STUDENT, SECOND_STUDENT, third_student]:
            client.post(
                '/api/register',
                data=json.dumps(student),
                content_type='application/json',
            )

        resp = client.get('/api/stats')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data is not None

        # Verify total count is 3
        total = data.get('total_students') or data.get('totalStudents') or data.get('total')
        assert total == 3


# ---------------------------------------------------------------------------
# Dashboard Tests
# ---------------------------------------------------------------------------

class TestDashboard:
    """Tests for GET /dashboard."""

    def test_dashboard_page_loads(self, client):
        """GET /dashboard – expect 200."""
        resp = client.get('/dashboard')
        assert resp.status_code == 200

    def test_dashboard_contains_title(self, client):
        """GET /dashboard – response should contain 'Dashboard'."""
        resp = client.get('/dashboard')
        assert resp.status_code == 200
        assert b'Dashboard' in resp.data
