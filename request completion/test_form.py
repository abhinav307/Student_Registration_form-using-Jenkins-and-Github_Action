import os
import pytest
from bs4 import BeautifulSoup

# Path to the HTML form file
HTML_FILE_PATH = os.path.join(os.path.dirname(__file__), "index.html")

@pytest.fixture(scope="module")
def html_soup():
    """Loads and parses the HTML file with BeautifulSoup."""
    assert os.path.exists(HTML_FILE_PATH), f"Error: {HTML_FILE_PATH} does not exist!"
    with open(HTML_FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    return BeautifulSoup(content, "html.parser")

class TestHtmlFormVerification:
    """Test suite to verify presence and configuration of the HTML form and its fields."""

    def test_html_file_exists(self):
        """Verify that the index.html file exists in the directory."""
        assert os.path.exists(HTML_FILE_PATH), "index.html file was not found."

    def test_form_element_presence(self, html_soup):
        """Verify that a <form> element is present in the document."""
        form = html_soup.find("form")
        assert form is not None, "Form element '<form>' is missing from index.html."
        assert form.get("id") == "contactForm" or form.get("method") is not None, "Form element should have valid attributes."

    def test_name_field_presence(self, html_soup):
        """Verify that the Name input field is present and configured."""
        name_input = html_soup.find("input", {"id": "name"}) or html_soup.find("input", {"name": "name"})
        assert name_input is not None, "Name input field is missing."
        assert name_input.get("type") in ["text", None], "Name field type must be 'text'."
        assert name_input.has_attr("required"), "Name field must have the 'required' attribute."

    def test_email_field_presence(self, html_soup):
        """Verify that the Email input field is present and configured."""
        email_input = html_soup.find("input", {"id": "email"}) or html_soup.find("input", {"name": "email"})
        assert email_input is not None, "Email input field is missing."
        assert email_input.get("type") == "email", "Email field type must be 'email'."
        assert email_input.has_attr("required"), "Email field must have the 'required' attribute."

    def test_contact_number_field_presence(self, html_soup):
        """Verify that the Contact Number input field is present and configured."""
        contact_input = html_soup.find("input", {"id": "contactNumber"}) or html_soup.find("input", {"name": "contactNumber"})
        assert contact_input is not None, "Contact Number input field is missing."
        assert contact_input.get("type") in ["tel", "text", "number"], "Contact Number type must be 'tel' or 'text'."
        assert contact_input.has_attr("required"), "Contact Number field must have the 'required' attribute."

    def test_submit_button_presence(self, html_soup):
        """Verify that a Submit button is present in the form."""
        submit_btn = html_soup.find("button", {"type": "submit"}) or html_soup.find("input", {"type": "submit"})
        assert submit_btn is not None, "Submit button is missing from the form."
        assert "submit" in submit_btn.text.lower() or submit_btn.get("value", "").lower() == "submit", "Submit button text should contain 'Submit'."

    def test_form_labels_association(self, html_soup):
        """Verify that each required input has an associated label for accessibility."""
        labels = [label.get("for") for label in html_soup.find_all("label") if label.get("for")]
        assert "name" in labels, "Label for 'name' is missing."
        assert "email" in labels, "Label for 'email' is missing."
        assert "contactNumber" in labels, "Label for 'contactNumber' is missing."
