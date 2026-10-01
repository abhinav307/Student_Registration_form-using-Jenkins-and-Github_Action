"""
test_html.py
============
Automated tests for the Student Registration Form (index.html).
Verifies file existence and the presence of all required form elements.

Run with:  python -m pytest tests/ -v
"""

import os
import re
import pytest

# ── Path to the HTML file under test ──
HTML_FILE = os.path.join(os.path.dirname(__file__), '..', 'index.html')


@pytest.fixture(scope='module')
def html_content():
    """Read the HTML file once for the entire test module."""
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        return f.read()


# ════════════════════════════════════════
#  1. FILE EXISTENCE
# ════════════════════════════════════════

class TestFileExistence:
    """Ensure the HTML file exists and is non-empty."""

    def test_file_exists(self):
        assert os.path.isfile(HTML_FILE), f"index.html not found at {HTML_FILE}"

    def test_file_not_empty(self, html_content):
        assert len(html_content.strip()) > 0, "index.html is empty"


# ════════════════════════════════════════
#  2. DOCUMENT STRUCTURE
# ════════════════════════════════════════

class TestDocumentStructure:
    """Check basic HTML5 document structure."""

    def test_has_doctype(self, html_content):
        assert '<!DOCTYPE html>' in html_content or '<!doctype html>' in html_content.lower()

    def test_has_html_tag(self, html_content):
        assert '<html' in html_content.lower()

    def test_has_head_tag(self, html_content):
        assert '<head>' in html_content.lower() or '<head ' in html_content.lower()

    def test_has_body_tag(self, html_content):
        assert '<body>' in html_content.lower() or '<body ' in html_content.lower()

    def test_has_title(self, html_content):
        assert '<title>' in html_content.lower(), "Missing <title> tag"

    def test_title_contains_registration(self, html_content):
        title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
        assert title_match, "Could not extract <title> content"
        assert 'registration' in title_match.group(1).lower()


# ════════════════════════════════════════
#  3. FORM ELEMENT
# ════════════════════════════════════════

class TestFormElement:
    """Verify the registration form exists."""

    def test_has_form_tag(self, html_content):
        assert '<form' in html_content.lower(), "Missing <form> element"

    def test_form_has_id(self, html_content):
        assert 'id="registrationForm"' in html_content, "Form missing id='registrationForm'"


# ════════════════════════════════════════
#  4. REQUIRED INPUT FIELDS
# ════════════════════════════════════════

class TestRequiredFields:
    """All mandatory form fields must be present."""

    @pytest.mark.parametrize("field_id", [
        "firstName",
        "lastName",
        "email",
        "phone",
        "dob",
    ])
    def test_input_field_exists(self, html_content, field_id):
        pattern = rf'id="{field_id}"'
        assert re.search(pattern, html_content), f"Missing input with id='{field_id}'"

    def test_gender_radio_buttons(self, html_content):
        radios = re.findall(r'name="gender"', html_content)
        assert len(radios) >= 2, "Need at least 2 gender radio buttons"

    @pytest.mark.parametrize("select_id", ["course", "semester"])
    def test_select_field_exists(self, html_content, select_id):
        assert f'id="{select_id}"' in html_content, f"Missing <select> with id='{select_id}'"

    def test_terms_checkbox(self, html_content):
        assert 'id="terms"' in html_content, "Missing terms & conditions checkbox"


# ════════════════════════════════════════
#  5. SUBMIT BUTTON
# ════════════════════════════════════════

class TestSubmitButton:
    """Ensure a submit button is present."""

    def test_has_submit_button(self, html_content):
        has_btn = (
            'type="submit"' in html_content
            or "type='submit'" in html_content
        )
        assert has_btn, "Missing submit button"

    def test_submit_button_has_id(self, html_content):
        assert 'id="submitBtn"' in html_content, "Submit button missing id='submitBtn'"


# ════════════════════════════════════════
#  6. INPUT TYPES & ATTRIBUTES
# ════════════════════════════════════════

class TestInputAttributes:
    """Verify correct input types and validation attributes."""

    def test_email_type(self, html_content):
        email_block = re.search(r'id="email"[^>]*', html_content)
        assert email_block, "Email field not found"
        assert 'type="email"' in html_content, "Email field should have type='email'"

    def test_phone_type(self, html_content):
        assert 'type="tel"' in html_content, "Phone field should have type='tel'"

    def test_dob_type(self, html_content):
        assert 'type="date"' in html_content, "DOB field should have type='date'"

    def test_required_attributes(self, html_content):
        """At least 5 fields should have the 'required' attribute."""
        required_count = len(re.findall(r'\brequired\b', html_content))
        assert required_count >= 5, f"Expected ≥5 required attributes, found {required_count}"


# ════════════════════════════════════════
#  7. STYLING & UX
# ════════════════════════════════════════

class TestStylingAndUX:
    """Basic checks for embedded styles and interactivity."""

    def test_has_style_tag(self, html_content):
        assert '<style>' in html_content.lower() or 'stylesheet' in html_content.lower()

    def test_has_script_tag(self, html_content):
        assert '<script>' in html_content.lower() or '<script ' in html_content.lower()

    def test_responsive_meta(self, html_content):
        assert 'viewport' in html_content.lower(), "Missing viewport meta tag for responsiveness"


# ════════════════════════════════════════
#  8. COURSE OPTIONS
# ════════════════════════════════════════

class TestCourseOptions:
    """Verify course dropdown has meaningful options."""

    def test_minimum_course_options(self, html_content):
        course_section = re.search(
            r'id="course".*?</select>', html_content, re.DOTALL | re.IGNORECASE
        )
        assert course_section, "Course <select> not found"
        options = re.findall(r'<option', course_section.group())
        # At least 4 real options + 1 placeholder
        assert len(options) >= 5, f"Expected ≥5 course <option>s, found {len(options)}"
