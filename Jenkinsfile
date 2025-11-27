pipeline {
    agent any

    environment {
        IMAGE_NAME = "pytest-lab"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    sh """
                    docker run --rm \
                        -v ${WORKSPACE}:/app \
                        -w /opt/calc \
                        ${IMAGE_NAME} \
                        pytest tests/unit --junitxml=unit_test_report.xml
                    """
                }
            }

            post {
                always {
                    junit 'unit_test_report.xml'
                }
            }
        }

        stage('Run REST Tests') {
            steps {
                script {
                    sh """
                    docker run --rm \
                        -v ${WORKSPACE}:/app \
                        -w /opt/calc \
                        ${IMAGE_NAME} \
                        pytest tests/rest --junitxml=api_test_report.xml
                    """
                }
            }

            post {
                always {
                    junit 'api_test_report.xml'
                }
            }
        }

        stage('Run BDD Tests') {
            steps {
                script {
                    sh """
                    docker run --rm \
                        -v ${WORKSPACE}:/app \
                        -w /opt/calc \
                        ${IMAGE_NAME} \
                        pytest tests/behavior --junitxml=bdd_test_report.xml || true
                    """
                }
            }

            post {
                always {
                    junit 'bdd_test_report.xml'
                }
            }
        }

        stage('Run E2E (Cypress)') {
            steps {
                dir('tests/e2e') {
                    sh """
                    npm install
                    npx cypress run || true
                    """
                }
            }

            post {
                always {
                    archiveArtifacts artifacts: 'tests/e2e/cypress/videos/**/*', allowEmptyArchive: true
                }
            }
        }

        stage('Run JMeter Tests') {
            steps {
                dir('tests/jmeter') {
                    sh """
                    docker build -t jmeter-test .
                    docker run --rm jmeter-test
                    """
                }
            }
        }

    }

    post {
        always {
            echo "Pipeline completado."
        }
    }
}
