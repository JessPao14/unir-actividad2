pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'docker run --rm -v $PWD:/workspace -w /workspace python:3.11 bash -c "pip install -r /workspace/requirements.txt && mkdir -p results/unit && pytest --junitxml=results/unit/unit_result.xml tests/unit/"'
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
