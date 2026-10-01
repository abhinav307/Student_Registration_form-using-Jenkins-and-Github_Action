/*
 * ════════════════════════════════════════════════════════════════
 *  Jenkinsfile — Student Registration Form CI Pipeline (Full-Stack)
 * ════════════════════════════════════════════════════════════════
 *  Stages:
 *    1. Checkout          → Pull latest code
 *    2. Verify Files      → Confirm all project files exist
 *    3. Validate HTML     → Check required form elements
 *    4. Setup Python      → Install Flask + pytest
 *    5. Run HTML Tests    → Validate HTML structure
 *    6. Run API Tests     → Test all REST endpoints
 *    7. Report            → Publish test results
 * ════════════════════════════════════════════════════════════════
 */

pipeline {
    agent any

    environment {
        HTML_FILE = 'index.html'
    }

    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        // ── Stage 1: Checkout ──
        stage('Checkout') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
            }
        }

        // ── Stage 2: Verify All Project Files ──
        stage('Verify Project Files') {
            steps {
                echo '📄 Verifying project files...'
                script {
                    def requiredFiles = [
                        'index.html',
                        'app.py',
                        'requirements.txt',
                        'Jenkinsfile',
                        'templates/dashboard.html',
                        'tests/test_html.py',
                        'tests/test_api.py',
                    ]

                    def missing = []
                    requiredFiles.each { f ->
                        if (fileExists(f)) {
                            echo "  ✅ Found: ${f}"
                        } else {
                            echo "  ❌ Missing: ${f}"
                            missing.add(f)
                        }
                    }

                    if (missing.size() > 0) {
                        error("❌ ${missing.size()} file(s) missing: ${missing}")
                    }

                    echo '🎉 All project files verified!'
                }
            }
        }

        // ── Stage 3: Validate Required HTML Elements ──
        stage('Validate HTML Elements') {
            steps {
                echo '🔍 Validating required form elements...'
                script {
                    def htmlContent = readFile(env.HTML_FILE)
                    def errors = []

                    def requiredElements = [
                        ['<form',            '<form> tag'],
                        ['id="firstName"',   'First Name input'],
                        ['id="lastName"',    'Last Name input'],
                        ['id="email"',       'Email input'],
                        ['id="phone"',       'Phone input'],
                        ['id="dob"',         'Date of Birth input'],
                        ['name="gender"',    'Gender radio buttons'],
                        ['id="course"',      'Course dropdown'],
                        ['id="semester"',    'Semester dropdown'],
                        ['type="submit"',    'Submit button'],
                        ['id="terms"',       'Terms checkbox'],
                        ['<title>',          '<title> tag'],
                        ['/api/register',    'API endpoint reference'],
                    ]

                    requiredElements.each { item ->
                        if (!htmlContent.contains(item[0])) {
                            errors.add("  ❌ Missing: ${item[1]}")
                        } else {
                            echo "  ✅ Found: ${item[1]}"
                        }
                    }

                    if (errors.size() > 0) {
                        errors.each { echo it }
                        error("❌ ${errors.size()} required element(s) missing!")
                    }

                    echo '🎉 All required HTML elements verified!'
                }
            }
        }

        // ── Stage 4: Setup Python & Install Dependencies ──
        stage('Setup Python') {
            steps {
                echo '🐍 Setting up Python environment...'
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv venv
                            . venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            python -m venv venv
                            call venv\\Scripts\\activate.bat
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        // ── Stage 5: Run HTML Tests ──
        stage('Run HTML Tests') {
            steps {
                echo '🧪 Running HTML validation tests...'
                script {
                    if (isUnix()) {
                        sh '''
                            . venv/bin/activate
                            python -m pytest tests/test_html.py -v --tb=short --junitxml=html-test-results.xml
                        '''
                    } else {
                        bat '''
                            call venv\\Scripts\\activate.bat
                            python -m pytest tests/test_html.py -v --tb=short --junitxml=html-test-results.xml
                        '''
                    }
                }
            }
        }

        // ── Stage 6: Run API Tests ──
        stage('Run API Tests') {
            steps {
                echo '🧪 Running API tests...'
                script {
                    if (isUnix()) {
                        sh '''
                            . venv/bin/activate
                            python -m pytest tests/test_api.py -v --tb=short --junitxml=api-test-results.xml
                        '''
                    } else {
                        bat '''
                            call venv\\Scripts\\activate.bat
                            python -m pytest tests/test_api.py -v --tb=short --junitxml=api-test-results.xml
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            echo '📊 Publishing test results...'
            junit allowEmptyResults: true, testResults: '*-test-results.xml'
        }
        success {
            echo '''
            ════════════════════════════════════
              ✅ BUILD SUCCESSFUL
              All HTML + API tests passed!
            ════════════════════════════════════
            '''
        }
        failure {
            echo '''
            ════════════════════════════════════
              ❌ BUILD FAILED
              Check the logs for details.
            ════════════════════════════════════
            '''
        }
        cleanup {
            echo '🧹 Cleaning up workspace...'
            cleanWs()
        }
    }
}
