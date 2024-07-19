pipeline {
    agent any
    environment {
        SECRET_KEY = credentials('jenkins-secret-key-id')
        DB_USERNAME = 'calendar-app'
        DB_PASSWORD = 'hue882gjng'
        DB_HOST = 'mongodb'
        DB_DATABASE = 'calendar_db'
        DB_PORT = '27017'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Loli2601/weekly_calendar_app.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("hilabarak/app_py:latest")
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        docker.image("hilabarak/app_py:latest").push()
                    }
                }
            }
        }
        stage('Deploy with Helm') {
            steps {
                script {
                    sh 'helm upgrade --install calendar-app ./my-flask-app --namespace default'
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
