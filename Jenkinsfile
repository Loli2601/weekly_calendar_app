pipeline {
    agent any

    environment {
        SECRET_KEY = credentials('jenkins-secret-key-id')
        DB_USERNAME = credentials('jenkins-db-username-id')
        DB_PASSWORD = credentials('jenkins-db-password-id')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Loli2601/weekly_calendar_app.git'
            }
        }

        stage('Build Image') {
            steps {
                script {
                    def image = docker.build("hilabarak/app_py:${env.BUILD_ID}")
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    docker.image("hilabarak/app_py:${env.BUILD_ID}").inside {
                        // Add your test commands here
                        sh 'echo Running tests...'
                    }
                }
            }
        }

        stage('Merge Changes') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh '''
                    git config user.email "jenkins@company.com"
                    git config user.name "Jenkins CI"
                    git fetch origin
                    git checkout -b merge-branch
                    git merge origin/develop --no-ff -m "Merging changes from develop branch"
                    git push origin merge-branch
                    '''
                }
            }
        }

        stage('Push to Main') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh '''
                    git checkout main
                    git merge merge-branch
                    git push origin main
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
