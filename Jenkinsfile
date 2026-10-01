/*
 * ════════════════════════════════════════════════════════════════
 *  Jenkinsfile — Student Registration Form CI Pipeline
 * ════════════════════════════════════════════════════════════════
 *  Stages:
 *    1. Checkout        → Pull latest code
 *    2. Verify HTML     → Confirm index.html exists
 *    3. Validate HTML   → Check required form elements
 *    4. Setup Python    → Install pytest
 *    5. Run Tests       → Execute pytest test suite
 *    6. Report          → Publish test results
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

        // ── Stage 2: Verify HTML File Exists ──
        stage('Verify HTML File') {
            steps {
                echo "📄 Verifying ${env.HTML_FILE} exists..."
                script {
                    if (!fileExists(env.HTML_FILE)) {
                        error("❌ ${env.HTML_FILE} not found in workspace!")
                    }
                    echo "✅ ${env.HTML_FILE} found."
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
                            pip install pytest
                        '''
                    } else {
                        bat '''
                            python -m venv venv
                            call venv\\Scripts\\activate.bat
                            pip install --upgrade pip
                            pip install pytest
                        '''
                    }
                }
            }
        }

        // ── Stage 5: Run Pytest Suite ──
        stage('Run Tests') {
            steps {
                echo '🧪 Running pytest test suite...'
                script {
                    if (isUnix()) {
                        sh '''
                            . venv/bin/activate
                            python -m pytest tests/ -v --tb=short --junitxml=test-results.xml
                        '''
                    } else {
                        bat '''
                            call venv\\Scripts\\activate.bat
                            python -m pytest tests/ -v --tb=short --junitxml=test-results.xml
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            echo '📊 Publishing test results...'
            junit allowEmptyResults: true, testResults: 'test-results.xml'
        }
        success {
            echo '''
            ════════════════════════════════════
              ✅ BUILD SUCCESSFUL
              All tests passed!
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
