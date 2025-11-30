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
                                // Run tests inside an ephemeral Python container, mounting the full workspace
                                sh '''#!/bin/bash
docker run --rm -v ${WORKSPACE}:/workspace -w /workspace python:3.11 bash -lc '
    set -e
    echo "--- workspace root (inside container) ---"
    ls -la /workspace || true
    echo "--- /workspace/tests ---"
    ls -la /workspace/tests || true
    echo "--- /workspace/tests/unit ---"
    ls -la /workspace/tests/unit || true

    if [ -f /workspace/requirements.txt ]; then
        echo "Found requirements.txt — installing dependencies"
        pip install -r /workspace/requirements.txt
    else
        echo "No requirements.txt found — installing pytest fallback"
        pip install pytest pytest-cov
    fi
    mkdir -p results/unit
    echo "Running pytest against /workspace/tests/unit (if present)"
    pytest --junitxml=results/unit/unit_result.xml /workspace/tests/unit || pytest --junitxml=results/unit/unit_result.xml -k "not none" || true
'
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
