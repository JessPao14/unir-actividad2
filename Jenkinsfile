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
                        # Copy workspace into container via tar stream to avoid volume mount issues.
                        # Run tests inside /workspace and stream back the results/unit directory.
                        tar -C "${WORKSPACE}" -cf - . | \
                        docker run --rm -i python:3.11 bash -lc '
                            set -e
                            mkdir -p /workspace
                            # extract incoming workspace tar
                            tar -xf - -C /workspace
                            # send diagnostics to stderr so stdout remains a pure tar stream
                            >&2 echo "--- Docker extracted workspace ---"
                            ls -la /workspace >&2 || true
                            # ensure we run from workspace so pytest writes into /workspace/results
                            cd /workspace
                            if [ -f requirements.txt ]; then
                                python -m pip install -q -r requirements.txt >&2
                            else
                                python -m pip install -q pytest pytest-cov >&2
                            fi
                            # run pytest without hard-coded paths so it auto-discovers tests
                            python -m pytest --junitxml=results/unit/unit_result.xml >&2 || true
                            # stream results back to host (only tar bytes on stdout)
                            if [ -d results/unit ]; then
                                tar -C /workspace -cf - results/unit
                            fi
                        ' | {
                            # extract any returned results back into workspace on the agent
                            set -e
                            # if there's tar data on stdin, extract it into the workspace
                            tar -xf - -C "${WORKSPACE}" || true
                        }
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
                    # run pytest without a rigid path so it discovers tests wherever they are
                    $PYTHON_CMD -m pytest --junitxml=results/unit/unit_result.xml || true
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
