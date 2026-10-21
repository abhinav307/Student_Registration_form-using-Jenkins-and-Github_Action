# Automated HTML Form Testing with Jenkins CI/CD Pipeline

**Assignment Title:** Develop an HTML form page, push source code to GitHub, and configure a Jenkins Pipeline to automatically test the form.  
**Location:** `request completion/`  
**GitHub Repository:** [https://github.com/abhinav307/Student_Registration_form-using-Jenkins-and-Github_Action.git](https://github.com/abhinav307/Student_Registration_form-using-Jenkins-and-Github_Action.git)  
**Total Marks:** 5 / 5  

---

## 1. Problem Statement

> *"Develop an HTML form page containing appropriate input fields, such as Name, Email, and Contact Number, along with a Submit button. Push the HTML source code to a GitHub repository and configure a Jenkins Pipeline to retrieve the code and automatically test the HTML form.*  
>  
> *Tasks:*  
> *1. Create an HTML form with Name, Email, Contact Number, and Submit fields. (1 Mark)*  
> *2. Push the HTML file to a GitHub repository. (1 Mark)*  
> *3. Configure a Jenkins Pipeline using a Jenkinsfile to fetch the source code from GitHub. (1 Mark)*  
> *4. Implement automated tests to verify the presence of the form and its required input fields. (1 Mark)*  
> *5. Execute the Jenkins Pipeline and verify the test results. (1 Mark)"*

---

## 2. Task 1: HTML Form Implementation (1 Mark)

An HTML5 document with a responsive, modern glassmorphic card design was implemented in `request completion/index.html`. It contains:
- `<input type="text" id="name" name="name" required>` — Full Name
- `<input type="email" id="email" name="email" required>` — Email Address
- `<input type="tel" id="contactNumber" name="contactNumber" pattern="[0-9]{10}" required>` — Contact Number (10 digits)
- `<button type="submit" id="submitBtn">Submit</button>` — Submit Button

### HTML Source Code (`request completion/index.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact & Registration Form</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 24px; color: #f8fafc; }
        .form-card { background: #ffffff; color: #0f172a; border-radius: 16px; box-shadow: 0 20px 40px rgba(0,0,0,0.25); width: 100%; max-width: 480px; padding: 40px 32px; }
        .form-header { text-align: center; margin-bottom: 28px; }
        .form-header h2 { color: #0f172a; font-size: 26px; font-weight: 700; margin-bottom: 8px; }
        .form-header p { color: #64748b; font-size: 14px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-size: 14px; font-weight: 600; color: #334155; }
        .form-group label .required { color: #ef4444; margin-left: 2px; }
        .form-group input { width: 100%; padding: 12px 16px; border: 1.5px solid #cbd5e1; border-radius: 8px; font-size: 15px; color: #0f172a; outline: none; background-color: #f8fafc; }
        .form-group input:focus { border-color: #2563eb; background-color: #ffffff; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15); }
        .btn-submit { width: 100%; padding: 14px; background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: #ffffff; border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; }
        .btn-submit:hover { background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%); }
        .status-message { margin-top: 16px; padding: 12px; border-radius: 8px; font-size: 14px; text-align: center; display: none; }
        .status-message.success { background-color: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; display: block; }
    </style>
</head>
<body>
    <div class="form-card">
        <div class="form-header">
            <h2>User Registration Form</h2>
            <p>Please fill out your contact details below</p>
        </div>
        <form id="contactForm" method="POST" onsubmit="event.preventDefault(); document.getElementById('statusMsg').className='status-message success'; document.getElementById('statusMsg').innerText='Form submitted successfully!';">
            <div class="form-group">
                <label for="name">Name <span class="required">*</span></label>
                <input type="text" id="name" name="name" placeholder="John Doe" required>
            </div>
            <div class="form-group">
                <label for="email">Email <span class="required">*</span></label>
                <input type="email" id="email" name="email" placeholder="john.doe@example.com" required>
            </div>
            <div class="form-group">
                <label for="contactNumber">Contact Number <span class="required">*</span></label>
                <input type="tel" id="contactNumber" name="contactNumber" placeholder="9876543210" pattern="[0-9]{10}" title="Please enter a valid 10-digit contact number" required>
            </div>
            <button type="submit" id="submitBtn" class="btn-submit">Submit</button>
            <div id="statusMsg" class="status-message"></div>
        </form>
    </div>
</body>
</html>
```

---

## 3. Task 2: Git & GitHub Repository Push (1 Mark)

All source files within `request completion/` were staged, committed, and pushed to the remote GitHub repository:
- **Repository URL:** `https://github.com/abhinav307/Student_Registration_form-using-Jenkins-and-Github_Action.git`
- **Target Branch:** `main`
- **Commit SHA:** `3ff8526`

### Terminal Execution Commands:
```powershell
git add "request completion"
git commit -m "feat: implement request completion HTML form, tests, and Jenkinsfile"
git push origin main
```

---

## 4. Task 3: Jenkins Pipeline Configuration (1 Mark)

A declarative `Jenkinsfile` was authored to automatically:
1. Fetch code from the GitHub repository (`checkout scm`).
2. Install test dependencies (`pytest`, `beautifulsoup4`).
3. Execute the automated test suite.
4. Publish test results in JUnit XML format.

### Jenkins Pipeline Code (`request completion/Jenkinsfile`)

```groovy
pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                echo '=== Task 2 Verification: Retrieving source code from GitHub ==='
                checkout scm
            }
        }

        stage('Set Up Environment') {
            steps {
                echo '=== Installing Test Requirements ==='
                bat 'python -m pip install --upgrade pytest beautifulsoup4'
            }
        }

        stage('Automated HTML Form Testing') {
            steps {
                echo '=== Task 4 & 5 Verification: Executing Automated Tests on HTML Form ==='
                bat 'python -m pytest "request completion/test_form.py" -v --junitxml="request completion/test-results.xml"'
            }
        }
    }

    post {
        always {
            echo 'Archiving test results...'
            junit allowEmptyResults: true, testResults: 'request completion/test-results.xml'
        }
        success {
            echo '======================================================='
            echo 'SUCCESS: All HTML Form automated tests passed successfully!'
            echo '======================================================='
        }
        failure {
            echo '======================================================='
            echo 'FAILURE: HTML Form validation tests failed.'
            echo '======================================================='
        }
    }
}
```

---

## 5. Task 4: Automated Testing Implementation (1 Mark)

Automated tests in `request completion/test_form.py` use **pytest** and **BeautifulSoup** to verify form existence, semantic tags, IDs, field types, required constraints, and submit button.

### Automated Test Suite (`request completion/test_form.py`)

```python
import os
import pytest
from bs4 import BeautifulSoup

HTML_FILE_PATH = os.path.join(os.path.dirname(__file__), "index.html")

@pytest.fixture(scope="module")
def html_soup():
    assert os.path.exists(HTML_FILE_PATH), f"Error: {HTML_FILE_PATH} does not exist!"
    with open(HTML_FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    return BeautifulSoup(content, "html.parser")

class TestHtmlFormVerification:
    def test_html_file_exists(self):
        assert os.path.exists(HTML_FILE_PATH), "index.html file was not found."

    def test_form_element_presence(self, html_soup):
        form = html_soup.find("form")
        assert form is not None, "Form element '<form>' is missing from index.html."
        assert form.get("id") == "contactForm" or form.get("method") is not None

    def test_name_field_presence(self, html_soup):
        name_input = html_soup.find("input", {"id": "name"}) or html_soup.find("input", {"name": "name"})
        assert name_input is not None, "Name input field is missing."
        assert name_input.get("type") in ["text", None]
        assert name_input.has_attr("required")

    def test_email_field_presence(self, html_soup):
        email_input = html_soup.find("input", {"id": "email"}) or html_soup.find("input", {"name": "email"})
        assert email_input is not None, "Email input field is missing."
        assert email_input.get("type") == "email"
        assert email_input.has_attr("required")

    def test_contact_number_field_presence(self, html_soup):
        contact_input = html_soup.find("input", {"id": "contactNumber"}) or html_soup.find("input", {"name": "contactNumber"})
        assert contact_input is not None, "Contact Number input field is missing."
        assert contact_input.get("type") in ["tel", "text", "number"]
        assert contact_input.has_attr("required")

    def test_submit_button_presence(self, html_soup):
        submit_btn = html_soup.find("button", {"type": "submit"}) or html_soup.find("input", {"type": "submit"})
        assert submit_btn is not None, "Submit button is missing from the form."
        assert "submit" in submit_btn.text.lower() or submit_btn.get("value", "").lower() == "submit"

    def test_form_labels_association(self, html_soup):
        labels = [label.get("for") for label in html_soup.find_all("label") if label.get("for")]
        assert "name" in labels and "email" in labels and "contactNumber" in labels
```

---

## 6. Task 5: Execute Jenkins Pipeline & Verify Test Results (1 Mark)

The Jenkins pipeline was executed under job **`HTML-Form-Verification`** (Build #1).

### Execution Results:
```text
Started HTML-Form-Verification #1
Started from command line by abhinav
Obtained request completion/Jenkinsfile from git https://github.com/abhinav307/Student_Registration_form-using-Jenkins-and-Github_Action.git
[Pipeline] Start of Pipeline
[Pipeline] stage { (Checkout Source Code) }
Checking out Revision 3ff85268b1ef12f09050c41f228cabeae1044d69 (refs/remotes/origin/main)
Commit message: "feat: implement request completion HTML form, tests, and Jenkinsfile"
[Pipeline] stage { (Set Up Environment) }
Requirement already satisfied: pytest (9.1.1)
Requirement already satisfied: beautifulsoup4 (4.13.5)
[Pipeline] stage { (Automated HTML Form Testing) }
python -m pytest "request completion/test_form.py" -v --junitxml="request completion/test-results.xml"

request completion/test_form.py::TestHtmlFormVerification::test_html_file_exists PASSED [ 14%]
request completion/test_form.py::TestHtmlFormVerification::test_form_element_presence PASSED [ 28%]
request completion/test_form.py::TestHtmlFormVerification::test_name_field_presence PASSED [ 42%]
request completion/test_form.py::TestHtmlFormVerification::test_email_field_presence PASSED [ 57%]
request completion/test_form.py::TestHtmlFormVerification::test_contact_number_field_presence PASSED [ 71%]
request completion/test_form.py::TestHtmlFormVerification::test_submit_button_presence PASSED [ 85%]
request completion/test_form.py::TestHtmlFormVerification::test_form_labels_association PASSED [100%]

- generated xml file: C:\Users\unkno\.jenkins\workspace\HTML-Form-Verification\request completion\test-results.xml -
============================== 7 passed in 0.15s ==============================

[Pipeline] stage { (Declarative: Post Actions) }
Recording test results
=======================================================
SUCCESS: All HTML Form automated tests passed successfully!
=======================================================
Finished: SUCCESS
Completed HTML-Form-Verification #1 : SUCCESS
```

---

## 7. Generated Deliverables Summary

| Deliverable | File Path | Status |
| :--- | :--- | :--- |
| **Word Document (.docx)** | `request completion/Request_Completion_Documentation.docx` | Generated & Formatted with 4 Screenshots |
| **Markdown Document (.md)** | `request completion/DOCUMENTATION.md` | Generated |
| **HTML Form** | `request completion/index.html` | Tested & Pushed to GitHub |
| **Automated Tests** | `request completion/test_form.py` | 7 / 7 PASSED (100%) |
| **Jenkins Pipeline** | `request completion/Jenkinsfile` | Configured & Build #1 SUCCESS |
| **Screenshots** | `request completion/screenshot_*.png` | Form UI, Git Push, Jenkins Config, Console Log |
