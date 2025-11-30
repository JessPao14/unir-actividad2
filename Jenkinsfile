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
                // Run pytest tests directly on agent (no Docker mounting issues)
                sh '''#!/bin/bash
                    set -e
                    echo "--- Current workspace ---"
                    pwd
                    ls -la tests/unit/ || echo "tests/unit not found"
                    
                    if [ -f requirements.txt ]; then
                        echo "Found requirements.txt — installing dependencies"
                        python3 -m pip install -q -r requirements.txt
                    else
                        echo "Installing pytest fallback"
                        python3 -m pip install -q pytest pytest-cov
                    fi
                    
                    mkdir -p results/unit
                    echo "Running pytest"
                    python3 -m pytest --junitxml=results/unit/unit_result.xml tests/unit/ || true
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
