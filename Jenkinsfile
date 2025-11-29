pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                script {
                    docker.image('python:3.11').inside {
                        sh 'pip install -r requirements.txt'
                        sh 'mkdir -p results/unit'
                        sh 'pytest --junitxml=results/unit/unit_result.xml tests/unit/'
                    }
                }
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
