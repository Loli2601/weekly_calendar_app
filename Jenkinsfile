pipeline {
    agent any
    environment {
        SECRET_KEY = '3f5eed7b6884e653ca2debd0653a92bfe9389a0351dd9589'
        DB_USERNAME = 'calendar-app'
        DB_PASSWORD = 'hue882gjng'
        DB_HOST = 'mongodb'
        DB_DATABASE = 'calendar_db'
        DB_PORT = '27017'
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
}
