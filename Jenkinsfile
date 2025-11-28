
pipeline {
    agent { label 'docker' }
    stages {
        stage('Source') {
            steps {
                git 'https://github.com/JessPao14/unir-actividad2.git'
            }
        }
        stage('Build') {
            steps {
                echo 'Building stage!'
                sh 'make build'
            }
        }
        stage('Unit tests') {
            steps {
                sh 'make test-unit'
                archiveArtifacts artifacts: 'results/unit/*.xml'
            }
        }
        stage('API tests') {
            steps {
                sh 'make test-api'
                archiveArtifacts artifacts: 'results/api/*.xml'
            }
        }
        stage('E2E tests') {
            steps {
                sh 'make test-e2e'
                archiveArtifacts artifacts: 'results/e2e/*.xml'
            }
        }
    }
    post {
        always {
            junit 'results/**/*_result.xml'
            cleanWs()
        }
        failure {
            echo "Sending email: Job ${env.JOB_NAME}, Build ${env.BUILD_NUMBER}"
            // mail to: 'tuemail@dominio.com', subject: "Pipeline Failed", body: "Job ${env.JOB_NAME}, Build ${env.BUILD_NUMBER}"
        }
    }
}
