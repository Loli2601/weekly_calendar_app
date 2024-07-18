pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "hilabarak/app_py:latest"
        DOCKER_REGISTRY_CREDENTIALS = 'dockerhub-credentials' // Set this in Jenkins
        KUBECONFIG_CREDENTIALS = 'kubeconfig-credentials' // Set this in Jenkins
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Loli2601/weekly_calendar_app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_REGISTRY_CREDENTIALS}") {
                        dockerImage.push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withCredentials([file(credentialsId: "${KUBECONFIG_CREDENTIALS}", variable: 'KUBECONFIG')]) {
                        sh """
                        helm upgrade --install my-flask-app ./my-flask-app --set image.repository=hilabarak/app_py --set image.tag=latest
                        """
                    }
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
