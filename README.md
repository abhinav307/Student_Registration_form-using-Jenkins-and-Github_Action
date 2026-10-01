# 🎓 Student Registration Form — CI/CD Project

> A college-level DevOps project: an HTML student registration form with automated testing via **GitHub Actions** and **Jenkins**.

---

## 📁 Project Structure

```
├── index.html                    # Student Registration Form (main page)
├── Jenkinsfile                   # Jenkins declarative pipeline
├── README.md                     # This file
│
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions CI workflow
│
└── tests/
    └── test_html.py              # Pytest test suite
```

---

## 🌐 Student Registration Form

A responsive, glassmorphism-styled registration form with:

- **Fields**: First Name, Last Name, Email, Phone, DOB, Gender, Course, Semester, Roll Number, Enrollment Year, Address
- **Validation**: Real-time client-side validation with error messages
- **UX**: Toast notification on successful submission, hover animations

### How to View

Simply open `index.html` in any modern browser.

---

## 🧪 Test Suite (`tests/test_html.py`)

The pytest suite validates **8 categories** with **20+ test cases**:

| Category               | What it checks                                      |
|------------------------|-----------------------------------------------------|
| File Existence         | `index.html` exists and is non-empty                |
| Document Structure     | `<!DOCTYPE>`, `<html>`, `<head>`, `<body>`, `<title>` |
| Form Element           | `<form>` tag with correct `id`                      |
| Required Fields        | All mandatory inputs (name, email, phone, DOB, etc.)|
| Submit Button          | Submit button presence and ID                       |
| Input Attributes       | Correct `type=` and `required` attributes           |
| Styling & UX           | `<style>`, `<script>`, viewport meta                |
| Course Options         | Dropdown has ≥5 course options                      |

### Run Tests Locally

```bash
pip install pytest
python -m pytest tests/ -v
```

---

## ⚙️ GitHub Actions CI

**File**: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

**Triggers**: Every `push` or `pull_request` to `main` / `master`.

**Pipeline Steps**:
1. Checkout code
2. Shell-based check: `index.html` exists
3. Shell-based grep: all required HTML elements present
4. Install Python 3.12 + pytest
5. Run full pytest suite
6. Print build summary

---

## 🏗️ Jenkins Pipeline

**File**: [`Jenkinsfile`](Jenkinsfile)

**Stages**:
1. **Checkout** — Pull latest code from SCM
2. **Verify HTML File** — Groovy `fileExists()` check
3. **Validate HTML Elements** — Groovy `readFile()` + content matching
4. **Setup Python** — Create venv, install pytest
5. **Run Tests** — Execute pytest with JUnit XML output
6. **Post Actions** — Publish JUnit results, print status, clean workspace

### Jenkins Setup

1. Install Jenkins with the **Pipeline** and **JUnit** plugins
2. Create a new **Pipeline** job
3. Under "Pipeline", select **Pipeline script from SCM**
4. Point to your Git repository
5. Jenkins will auto-detect the `Jenkinsfile` and run the pipeline

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone <your-repo-url>
cd <repo-name>

# 2. View the form
open index.html          # macOS
start index.html         # Windows
xdg-open index.html      # Linux

# 3. Run tests locally
pip install pytest
python -m pytest tests/ -v

# 4. Push to GitHub — CI runs automatically!
git add .
git commit -m "Initial commit: Student Registration Form with CI/CD"
git push origin main
```

---

## 📝 License

This project is for educational purposes. MIT License.
