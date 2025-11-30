pipeline {
    agent any
    stages {
        stage('Checkout repository') {
            steps {
                // Force a full checkout into the workspace (lightweight checkout may only fetch the Jenkinsfile)
                checkout scm
                sh 'ls -la'
            }
        }
        stage('Test') {
            steps {
                // Run pytest tests (try python3, then python, then Docker)
                sh '''#!/bin/bash
                    set -e
                    echo "--- Current workspace ---"
                    pwd
                    ls -la tests/unit/ || echo "tests/unit not found"
                    
                    mkdir -p results/unit
                    
                    # Detect Python executable
                    echo "--- Detecting Python executable ---"
                    PYTHON_CMD=""
                    if command -v python3 &> /dev/null; then
                        PYTHON_CMD="python3"
                        echo "✓ Found python3: $(python3 --version)"
                    elif command -v python &> /dev/null; then
                        PYTHON_CMD="python"
                        echo "✓ Found python: $(python --version)"
                    else
                        echo "✗ Python not found locally, attempting Docker tar-copy fallback..."
                        # Copy workspace into container via tar stream to avoid volume mount issues
                        tar -C "${WORKSPACE}" -cf - . | docker run --rm -i python:3.11 bash -lc '
                            mkdir -p /workspace && tar -xf - -C /workspace
                            echo "--- Docker extracted workspace ---"
                            ls -la /workspace || true
                            ls -la /workspace/tests/unit/ 2>/dev/null || echo "tests/unit not found"
                            pip install -q pytest pytest-cov
                            python -m pytest --junitxml=results/unit/unit_result.xml tests/unit/ || true
                        '
                        exit 0
                    fi
                    
                    echo "--- Using Python: $PYTHON_CMD ---"
                    
                    if [ -f requirements.txt ]; then
                        echo "✓ Found requirements.txt — installing dependencies"
                        $PYTHON_CMD -m pip install -q -r requirements.txt
                    else
                        echo "✗ No requirements.txt — installing pytest fallback"
                        $PYTHON_CMD -m pip install -q pytest pytest-cov
                    fi
                    
                    echo "--- Running pytest ---"
                    $PYTHON_CMD -m pytest --junitxml=results/unit/unit_result.xml tests/unit/ || true
                '''
            }
        }
        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'results/unit/*.xml', allowEmptyArchive: true
            }
        }
    }
    post {
        always {
            junit testResults: 'results/unit/*.xml', allowEmptyResults: true
        }
        failure {
            echo "Enviando correo: Job ${env.JOB_NAME}, Build ${env.BUILD_NUMBER} falló."
        }
    }
}
