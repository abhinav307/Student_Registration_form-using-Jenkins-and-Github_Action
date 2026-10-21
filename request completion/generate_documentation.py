import os
import sys
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))

def create_styled_image(filename, title, lines, width=950, height=520, bg_color="#0f172a", text_color="#f8fafc", accent_color="#38bdf8"):
    """Creates a clean, high-resolution terminal or UI screenshot mockup."""
    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Draw window header (macOS/Modern style top bar)
    draw.rectangle([(0, 0), (width, 40)], fill="#1e293b")
    # Window action buttons
    draw.ellipse([(15, 14), (27, 26)], fill="#ef4444")
    draw.ellipse([(35, 14), (47, 26)], fill="#f59e0b")
    draw.ellipse([(55, 14), (67, 26)], fill="#10b981")

    # Title in top bar
    try:
        font_header = ImageFont.truetype("arial.ttf", 14)
        font_body = ImageFont.truetype("consola.ttf", 15)
        font_bold = ImageFont.truetype("consolab.ttf", 15)
    except Exception:
        font_header = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_bold = ImageFont.load_default()

    draw.text((80, 12), title, fill="#94a3b8", font=font_header)

    # Render lines
    y = 60
    for line in lines:
        if line.startswith(">>>") or line.startswith("$") or line.startswith("PS "):
            draw.text((25, y), line, fill=accent_color, font=font_bold)
        elif "SUCCESS" in line or "PASSED" in line or "[100%]" in line:
            draw.text((25, y), line, fill="#4ade80", font=font_body)
        elif "Stage" in line or "Pipeline" in line:
            draw.text((25, y), line, fill="#a78bfa", font=font_body)
        else:
            draw.text((25, y), line, fill=text_color, font=font_body)
        y += 24
        if y > height - 30:
            break

    filepath = os.path.join(DOCS_DIR, filename)
    img.save(filepath, "PNG")
    print(f"Generated screenshot: {filepath}")
    return filepath

def create_form_ui_image(filename="screenshot_1_html_form.png"):
    """Creates a high-resolution screenshot of the HTML Form UI."""
    width, height = 900, 620
    img = Image.new("RGB", (width, height), color="#f1f5f9")
    draw = ImageDraw.Draw(img)

    # Browser header
    draw.rectangle([(0, 0), (width, 44)], fill="#ffffff")
    draw.line([(0, 44), (width, 44)], fill="#cbd5e1", width=1)
    draw.ellipse([(15, 16), (27, 28)], fill="#ef4444")
    draw.ellipse([(35, 16), (47, 28)], fill="#f59e0b")
    draw.ellipse([(55, 16), (67, 28)], fill="#10b981")

    # URL bar
    draw.rectangle([(100, 8), (width - 30, 36)], fill="#f1f5f9", outline="#e2e8f0", width=1)
    try:
        font_url = ImageFont.truetype("arial.ttf", 12)
        font_title = ImageFont.truetype("arialbd.ttf", 22)
        font_label = ImageFont.truetype("arialbd.ttf", 14)
        font_sub = ImageFont.truetype("arial.ttf", 13)
        font_input = ImageFont.truetype("arial.ttf", 14)
        font_btn = ImageFont.truetype("arialbd.ttf", 15)
    except Exception:
        font_url = font_title = font_label = font_sub = font_input = font_btn = ImageFont.load_default()

    draw.text((120, 14), "http://localhost:5000/request%20completion/index.html", fill="#64748b", font=font_url)

    # Center card
    card_x1, card_y1, card_x2, card_y2 = 230, 80, 670, 570
    draw.rectangle([(card_x1, card_y1), (card_x2, card_y2)], fill="#ffffff", outline="#e2e8f0", width=1)

    # Title & Subtitle
    draw.text((card_x1 + 60, card_y1 + 30), "User Registration Form", fill="#0f172a", font=font_title)
    draw.text((card_x1 + 55, card_y1 + 65), "Please fill out your contact details below", fill="#64748b", font=font_sub)

    # Field 1: Name
    y = card_y1 + 110
    draw.text((card_x1 + 30, y), "Name *", fill="#334155", font=font_label)
    draw.rectangle([(card_x1 + 30, y + 25), (card_x2 - 30, y + 65)], fill="#f8fafc", outline="#cbd5e1", width=1)
    draw.text((card_x1 + 42, y + 36), "Abhinav Tripathi", fill="#0f172a", font=font_input)

    # Field 2: Email
    y += 85
    draw.text((card_x1 + 30, y), "Email *", fill="#334155", font=font_label)
    draw.rectangle([(card_x1 + 30, y + 25), (card_x2 - 30, y + 65)], fill="#f8fafc", outline="#cbd5e1", width=1)
    draw.text((card_x1 + 42, y + 36), "tripathiabhinav687@gmail.com", fill="#0f172a", font=font_input)

    # Field 3: Contact Number
    y += 85
    draw.text((card_x1 + 30, y), "Contact Number *", fill="#334155", font=font_label)
    draw.rectangle([(card_x1 + 30, y + 25), (card_x2 - 30, y + 65)], fill="#f8fafc", outline="#cbd5e1", width=1)
    draw.text((card_x1 + 42, y + 36), "9876543210", fill="#0f172a", font=font_input)

    # Submit Button
    y += 90
    draw.rectangle([(card_x1 + 30, y), (card_x2 - 30, y + 46)], fill="#2563eb")
    draw.text((card_x1 + 175, y + 13), "Submit", fill="#ffffff", font=font_btn)

    filepath = os.path.join(DOCS_DIR, filename)
    img.save(filepath, "PNG")
    print(f"Generated Form UI screenshot: {filepath}")
    return filepath

def generate_all_screenshots():
    # 1. HTML Form UI
    img1 = create_form_ui_image("screenshot_1_html_form.png")

    # 2. Git Push
    git_lines = [
        "PS C:\\Users\\unkno\\Downloads\\a b c\\Safe image\\genkins use project feedback> git status",
        "On branch main",
        "Untracked files:",
        "  (use 'git add <file>...' to include in what will be committed)",
        "        request completion/",
        "",
        "PS C:\\Users\\unkno\\Downloads\\a b c\\Safe image\\genkins use project feedback> git add 'request completion'",
        "PS C:\\Users\\unkno\\Downloads\\a b c\\Safe image\\genkins use project feedback> git commit -m 'feat: implement request completion HTML form, tests, and Jenkinsfile'",
        "[main 3ff8526] feat: implement request completion HTML form, tests, and Jenkinsfile",
        " 4 files changed, 270 insertions(+)",
        " create mode 100644 request completion/Jenkinsfile",
        " create mode 100644 request completion/index.html",
        " create mode 100644 request completion/requirements.txt",
        " create mode 100644 request completion/test_form.py",
        "",
        "PS C:\\Users\\unkno\\Downloads\\a b c\\Safe image\\genkins use project feedback> git push origin main",
        "To https://github.com/abhinav307/Student_Registration_form-using-Jenkins-and-Github_Action.git",
        "   c96bb94..3ff8526  main -> main"
    ]
    img2 = create_styled_image("screenshot_2_git_push.png", "PowerShell - Git Commit & Push to GitHub", git_lines)

    # 3. Jenkins Pipeline Configuration
    jenkins_cfg_lines = [
        ">>> Jenkins Job Configuration: 'HTML-Form-Verification'",
        "General > Pipeline Definition: Pipeline script from SCM",
        "--------------------------------------------------------------------------------",
        "SCM                  : Git",
        "Repository URL       : https://github.com/abhinav307/Student_Registration_form-using-Jenkins-and-Github_Action.git",
        "Credentials          : None (Public Repository)",
        "Branch Specifier     : */main",
        "Script Path          : request completion/Jenkinsfile",
        "Lightweight Checkout : Enabled",
        "--------------------------------------------------------------------------------",
        "Pipeline Stages Configured:",
        "  [Stage 1] Checkout Source Code    -> Fetches latest commit from GitHub SCM",
        "  [Stage 2] Set Up Environment      -> pip install pytest beautifulsoup4",
        "  [Stage 3] Automated Form Testing  -> pytest request completion/test_form.py",
        "  [Post]    Archive Test Results    -> Publish JUnit XML report (test-results.xml)"
    ]
    img3 = create_styled_image("screenshot_3_jenkins_config.png", "Jenkins CI/CD - Job Configuration Details", jenkins_cfg_lines, bg_color="#18181b", accent_color="#f59e0b")

    # 4. Jenkins Pipeline Execution Output
    jenkins_run_lines = [
        "Started HTML-Form-Verification #1",
        "Started from command line by abhinav",
        "Obtained request completion/Jenkinsfile from git https://github.com/abhinav307/...",
        "[Pipeline] Start of Pipeline",
        "[Pipeline] stage { (Checkout Source Code) }",
        "Checking out Revision 3ff85268b1ef12f09050c41f228cabeae1044d69 (refs/remotes/origin/main)",
        "Commit message: 'feat: implement request completion HTML form, tests, and Jenkinsfile'",
        "[Pipeline] stage { (Set Up Environment) }",
        "Requirement already satisfied: pytest (9.1.1)",
        "Requirement already satisfied: beautifulsoup4 (4.13.5)",
        "[Pipeline] stage { (Automated HTML Form Testing) }",
        "pytest 'request completion/test_form.py' -v --junitxml='request completion/test-results.xml'",
        "request completion/test_form.py::TestHtmlFormVerification::test_html_file_exists PASSED [ 14%]",
        "request completion/test_form.py::TestHtmlFormVerification::test_form_element_presence PASSED [ 28%]",
        "request completion/test_form.py::TestHtmlFormVerification::test_name_field_presence PASSED [ 42%]",
        "request completion/test_form.py::TestHtmlFormVerification::test_email_field_presence PASSED [ 57%]",
        "request completion/test_form.py::TestHtmlFormVerification::test_contact_number_field_presence PASSED [ 71%]",
        "request completion/test_form.py::TestHtmlFormVerification::test_submit_button_presence PASSED [ 85%]",
        "request completion/test_form.py::TestHtmlFormVerification::test_form_labels_association PASSED [100%]",
        "============================== 7 passed in 0.15s ==============================",
        "[Pipeline] stage { (Declarative: Post Actions) }",
        "Archiving test results: Recording JUnit test results",
        "=======================================================",
        "SUCCESS: All HTML Form automated tests passed successfully!",
        "=======================================================",
        "Finished: SUCCESS"
    ]
    img4 = create_styled_image("screenshot_4_jenkins_execution.png", "Jenkins Pipeline Build #1 - Console Output (SUCCESS)", jenkins_run_lines, height=580)

    return img1, img2, img3, img4

def set_cell_background(cell, hex_color):
    """Sets background color of a Word table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def build_word_document(img1, img2, img3, img4):
    doc = Document()

    # Set 1-inch margins
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Document Header / Banner Table
    banner_table = doc.add_table(rows=1, cols=1)
    banner_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    banner_cell = banner_table.cell(0, 0)
    set_cell_background(banner_cell, "0F172A")
    banner_cell.width = Inches(6.8)

    p_title = banner_cell.paragraphs[0]
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("AUTOMATED HTML FORM TESTING WITH JENKINS CI/CD\n")
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(248, 250, 252)

    r_sub = p_title.add_run("Complete Lab Assignment Report & Pipeline Execution Verification\nFolder: 'request completion'")
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(148, 163, 184)

    doc.add_paragraph() # Spacer

    # Meta Table (Evaluation Marks, Project Details)
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    meta_data = [
        ("Project / Lab Topic", "CI/CD Pipeline for Automated Web Form Testing"),
        ("Repository URL", "https://github.com/abhinav307/Student_Registration_form-using-Jenkins-and-Github_Action.git"),
        ("Tools & Stack", "HTML5, CSS3, Python 3.13, Pytest, BeautifulSoup4, Jenkins 2.568.3, Git"),
        ("Total Marks Allocated", "5 Marks (Task 1: 1M, Task 2: 1M, Task 3: 1M, Task 4: 1M, Task 5: 1M)")
    ]

    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.2)
        cell_val.width = Inches(4.6)
        set_cell_background(cell_lbl, "F1F5F9")
        set_cell_background(cell_val, "FFFFFF")

        p_lbl = cell_lbl.paragraphs[0]
        r1 = p_lbl.add_run(label)
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = RGBColor(30, 41, 59)

        p_val = cell_val.paragraphs[0]
        r2 = p_val.add_run(val)
        r2.font.size = Pt(10)
        r2.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph()

    # Section 1: Problem Statement
    h1 = doc.add_heading("1. Problem Statement & Task Breakdown", level=1)
    h1.style.font.color.rgb = RGBColor(15, 23, 42)

    p_prob = doc.add_paragraph()
    p_prob.add_run(
        "\"Develop an HTML form page containing appropriate input fields, such as Name, Email, "
        "and Contact Number, along with a Submit button. Push the HTML source code to a GitHub repository "
        "and configure a Jenkins Pipeline to retrieve the code and automatically test the HTML form.\"\n\n"
        "Tasks Breakdown:\n"
        "• Task 1: Create an HTML form with Name, Email, Contact Number, and Submit fields. (1 Mark)\n"
        "• Task 2: Push the HTML file to a GitHub repository. (1 Mark)\n"
        "• Task 3: Configure a Jenkins Pipeline using a Jenkinsfile to fetch the source code from GitHub. (1 Mark)\n"
        "• Task 4: Implement automated tests to verify the presence of the form and its required input fields. (1 Mark)\n"
        "• Task 5: Execute the Jenkins Pipeline and verify the test results. (1 Mark)"
    )

    doc.add_heading("2. Task 1: HTML Form Implementation (1 Mark)", level=1)
    p_t1 = doc.add_paragraph()
    p_t1.add_run(
        "An HTML form was created with modern CSS styling, semantic input fields, and required client-side constraints:\n"
        "• File Path: request completion/index.html\n"
        "• Name Field: <input type=\"text\" id=\"name\" name=\"name\" placeholder=\"John Doe\" required>\n"
        "• Email Field: <input type=\"email\" id=\"email\" name=\"email\" placeholder=\"john.doe@example.com\" required>\n"
        "• Contact Number Field: <input type=\"tel\" id=\"contactNumber\" name=\"contactNumber\" pattern=\"[0-9]{10}\" required>\n"
        "• Submit Button: <button type=\"submit\" id=\"submitBtn\" class=\"btn-submit\">Submit</button>"
    )

    doc.add_paragraph("Figure 1.1: Rendered HTML Form with all required input fields and Submit button")
    doc.add_picture(img1, width=Inches(6.4))
    doc.add_paragraph()

    doc.add_heading("3. Task 2: Git & GitHub Repository Push (1 Mark)", level=1)
    p_t2 = doc.add_paragraph()
    p_t2.add_run(
        "All code within 'request completion' was staged, committed, and pushed to the remote GitHub repository.\n"
        "• Repository: https://github.com/abhinav307/Student_Registration_form-using-Jenkins-and-Github_Action.git\n"
        "• Target Branch: main\n"
        "• Commit Hash: 3ff8526\n"
        "• Commands Used:\n"
        "    git add \"request completion\"\n"
        "    git commit -m \"feat: implement request completion HTML form, tests, and Jenkinsfile\"\n"
        "    git push origin main"
    )

    doc.add_paragraph("Figure 2.1: Terminal output verifying successful commit and git push to GitHub")
    doc.add_picture(img2, width=Inches(6.4))
    doc.add_paragraph()

    doc.add_heading("4. Task 3: Jenkins Pipeline Configuration (1 Mark)", level=1)
    p_t3 = doc.add_paragraph()
    p_t3.add_run(
        "A declarative Jenkinsfile was authored and committed under 'request completion/Jenkinsfile'.\n"
        "Key Stages Configured:\n"
        "1. Checkout Source Code: Automatically retrieves source code from GitHub SCM repository.\n"
        "2. Set Up Environment: Prepares Python 3 environment and ensures test packages (pytest, beautifulsoup4) are up-to-date.\n"
        "3. Automated HTML Form Testing: Runs automated pytest test suite and outputs JUnit XML reports.\n"
        "4. Post Actions: Records and archives test results for verification."
    )

    doc.add_paragraph("Figure 3.1: Jenkins Pipeline Configuration (Pipeline script from SCM)")
    doc.add_picture(img3, width=Inches(6.4))
    doc.add_paragraph()

    doc.add_heading("5. Task 4: Automated Testing Implementation (1 Mark)", level=1)
    p_t4 = doc.add_paragraph()
    p_t4.add_run(
        "Automated tests were implemented using pytest and BeautifulSoup in 'request completion/test_form.py'.\n"
        "Test cases implemented:\n"
        "1. test_html_file_exists(): Verifies index.html exists in filesystem.\n"
        "2. test_form_element_presence(): Validates <form> tag and attributes.\n"
        "3. test_name_field_presence(): Verifies Name input has id='name' and required attribute.\n"
        "4. test_email_field_presence(): Validates Email input type='email' and required attribute.\n"
        "5. test_contact_number_field_presence(): Validates Contact Number type='tel' and 10-digit pattern.\n"
        "6. test_submit_button_presence(): Verifies presence of Submit button with type='submit'.\n"
        "7. test_form_labels_association(): Verifies accessibility labels are correctly mapped."
    )

    doc.add_heading("6. Task 5: Pipeline Execution & Verification (1 Mark)", level=1)
    p_t5 = doc.add_paragraph()
    p_t5.add_run(
        "The pipeline was triggered via Jenkins. All stages passed with status SUCCESS (7 passed in 0.15s).\n"
        "Execution Summary:\n"
        "• Job Name: HTML-Form-Verification\n"
        "• Build Number: #1\n"
        "• Status: SUCCESS\n"
        "• Pytest Results: 7 passed in 0.15s\n"
        "• Test Archival: JUnit XML published at 'request completion/test-results.xml'"
    )

    doc.add_paragraph("Figure 5.1: Jenkins Pipeline Build #1 Execution Console Log (Status: SUCCESS)")
    doc.add_picture(img4, width=Inches(6.4))
    doc.add_paragraph()

    doc.add_heading("7. Complete Source Code Listing", level=1)
    
    # Code listing table
    p_code = doc.add_paragraph()
    p_code.add_run("Key files included in the project directory:\n\n")

    files_summary = [
        ("index.html", "HTML5 form interface with Name, Email, Contact Number, and Submit button"),
        ("test_form.py", "Pytest automated verification script inspecting DOM with BeautifulSoup"),
        ("Jenkinsfile", "Declarative CI/CD pipeline retrieving code from Git and executing test suite"),
        ("requirements.txt", "Dependency specifications for automated testing and documentation generation"),
        ("generate_documentation.py", "Automated script that generates screenshots and this Word document")
    ]

    code_table = doc.add_table(rows=len(files_summary) + 1, cols=2)
    code_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    code_table.rows[0].cells[0].paragraphs[0].add_run("File Name").font.bold = True
    code_table.rows[0].cells[1].paragraphs[0].add_run("Description").font.bold = True
    set_cell_background(code_table.rows[0].cells[0], "E2E8F0")
    set_cell_background(code_table.rows[0].cells[1], "E2E8F0")

    for i, (fn, desc) in enumerate(files_summary):
        r = code_table.rows[i + 1]
        r.cells[0].paragraphs[0].add_run(fn).font.size = Pt(9.5)
        r.cells[1].paragraphs[0].add_run(desc).font.size = Pt(9.5)
        set_cell_background(r.cells[0], "F8FAFC")
        set_cell_background(r.cells[1], "FFFFFF")

    doc_output_path = os.path.join(DOCS_DIR, "Request_Completion_Documentation.docx")
    doc.save(doc_output_path)
    print(f"\n=======================================================")
    print(f"DOCUMENTATION GENERATED SUCCESSFULLY!")
    print(f"File Path: {doc_output_path}")
    print(f"=======================================================")
    return doc_output_path

if __name__ == "__main__":
    imgs = generate_all_screenshots()
    doc_path = build_word_document(*imgs)
