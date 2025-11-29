
pipeline {
    agent { node { label 'master' } }
    stages {
        stage('Source') {
            steps {
                echo 'Clonando el repositorio...'
                git 'https://github.com/JessPao14/unir-actividad2.git'
            }
        }
        stage('Dependencies') {
            steps {
                echo 'Instalando dependencias...'
                sh 'python -m pip install -q -r requirements.txt'
            }
        }
        stage('Unit Tests') {
            steps {
                echo 'Ejecutando pruebas unitarias reales...'
                sh '''
                    mkdir -p results/unit
                    pytest --junitxml=results/unit/unit_result.xml tests/unit/ || true
                '''
            }
        }
        stage('Archive Results') {
            steps {
                echo 'Archivando resultados...'
                archiveArtifacts artifacts: 'results/unit/*.xml', allowEmptyArchive: true
            }
        }
    }
    post {
        always {
            echo 'Publicando resultados JUnit...'
            junit testResults: 'results/unit/*.xml', allowEmptyResults: true
        }
        failure {
            echo "Enviando correo: Job ${env.JOB_NAME}, Build ${env.BUILD_NUMBER} falló."
            mail to: 'jsscsimba753@gmail.com', subject: "Pipeline Failed", body: "Job ${env.JOB_NAME}, Build ${env.BUILD_NUMBER}"
        }
    }
}
