pipeline {
    agent {
        docker {
            image 'python:3.11'
            args '-v $PWD:/workspace'
        }
    }
    stages {
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'mkdir -p results/unit'
                sh 'pytest --junitxml=results/unit/unit_result.xml tests/unit/'
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
