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
docker run --rm -v $PWD:/workspace -w /workspace python:3.11 bash -lc '
    set -e
    if [ -f /workspace/requirements.txt ]; then
        echo "Found requirements.txt — installing dependencies"
        pip install -r /workspace/requirements.txt
    else
        echo "No requirements.txt found — installing pytest fallback"
        pip install pytest pytest-cov
    fi
    mkdir -p results/unit
    pytest --junitxml=results/unit/unit_result.xml tests/unit/
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
