# 🎓 Student Registration Form — Full-Stack CI/CD Project

> A college-level DevOps project: **Flask backend** + **SQLite database** + **HTML frontend** + **Admin Dashboard** — with automated testing via **GitHub Actions** and **Jenkins**.

---

## 📁 Project Structure

```
├── app.py                        # Flask backend (REST API + SQLite)
├── index.html                    # Student Registration Form (frontend)
├── requirements.txt              # Python dependencies (Flask, pytest)
├── Jenkinsfile                   # Jenkins declarative pipeline
├── README.md                     # This file
│
├── templates/
│   └── dashboard.html            # Admin Dashboard (view/search/delete students)
│
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions CI workflow
│
└── tests/
    ├── test_html.py              # HTML validation tests (29 tests)
    └── test_api.py               # API endpoint tests (17 tests)
```

---

## 🌐 Features

### Student Registration Form (`index.html`)
- Glassmorphism UI with responsive grid layout
- **Fields**: First Name, Last Name, Email, Phone, DOB, Gender, Course, Semester, Roll Number, Enrollment Year, Address
- Real-time client-side validation with error messages
- Submits data to Flask API via `fetch()` — data is **saved to database**
- Toast notification on success/error

### Flask Backend (`app.py`)
- **REST API** with full CRUD operations
- **SQLite** database — zero setup required
- Server-side validation (email format, phone digits, required fields)
- CORS support
- Error handling on all endpoints

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serve registration form |
| `GET` | `/dashboard` | Serve admin dashboard |
| `POST` | `/api/register` | Register a new student |
| `GET` | `/api/students` | Get all students (supports `?search=`) |
| `GET` | `/api/students/<id>` | Get single student |
| `DELETE` | `/api/students/<id>` | Delete a student |
| `GET` | `/api/stats` | Get aggregate statistics |

### Admin Dashboard (`templates/dashboard.html`)
- View all registered students in a searchable table
- Real-time search/filter
- Delete students with confirmation
- Stats cards: Total Students, Popular Course, Gender Distribution
- Same glassmorphism dark theme as registration form

---

## 🧪 Test Suite — 46 Tests

### HTML Tests (`tests/test_html.py`) — 29 tests
| Category | What it checks |
|----------|---------------|
| File Existence | `index.html` exists and is non-empty |
| Document Structure | `<!DOCTYPE>`, `<html>`, `<head>`, `<body>`, `<title>` |
| Form Element | `<form>` tag with correct `id` |
| Required Fields | All mandatory inputs |
| Submit Button | Submit button presence |
| Input Attributes | Correct `type=` and `required` attributes |
| Styling & UX | `<style>`, `<script>`, viewport meta |
| Course Options | ≥5 course options |

### API Tests (`tests/test_api.py`) — 17 tests
| Category | What it checks |
|----------|---------------|
| Registration | Success, missing fields, invalid email/phone, duplicate email |
| Get Students | Empty list, after register, search, single, nonexistent |
| Delete Student | Delete existing, delete nonexistent |
| Stats | Empty stats, stats with data |
| Dashboard | Page loads, contains title |

### Run Tests Locally

```bash
pip install -r requirements.txt
python -m pytest tests/ -v
```

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/abhinav307/Student_Registration_form-using-Jenkins-and-Github_Action.git
cd Student_Registration_form-using-Jenkins-and-Github_Action

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
python app.py

# 4. Open in browser
#    Registration Form: http://localhost:5000
#    Admin Dashboard:   http://localhost:5000/dashboard

# 5. Run tests
python -m pytest tests/ -v
```

---

## ⚙️ CI/CD Pipelines

### GitHub Actions
- Triggers on every push/PR to `main`
- Validates HTML structure, installs dependencies, runs all 46 tests

### Jenkins
- 6-stage pipeline: Checkout → Verify Files → Validate HTML → Setup Python → HTML Tests → API Tests
- JUnit XML reports published automatically

---

## 📝 License

This project is for educational purposes. MIT License.
