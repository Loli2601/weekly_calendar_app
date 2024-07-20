pipeline {
    agent any

    environment {
        SECRET_KEY = credentials('jenkins-secret-key-id')
        DB_USERNAME = credentials('jenkins-db-username-id')
        DB_PASSWORD = credentials('jenkins-db-password-id')
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'docker build -t hilabarak/app_py:latest .'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                // Add your test steps here
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                sh 'helm upgrade --install calendar-app ./my-flask-app'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
