pipeline {
    agent {
        kubernetes {
            yamlFile 'runner.yaml'
            defaultContainer 'builder'
        }
    }

    environment {
        LOGGING_ID = '11cbcb73-1cd6-45ac-b5ca-3f90cbff2a7e'
        DOCKER_IMAGE = 'hilabarak/weekly_calendar_app'
        DOCKERHUB_URL = 'https://registry.hub.docker.com'
        GITHUB_API_URL = 'https://api.github.com' // For pull requests
        GITHUB_REPO = 'Loli2601/weekly_calendar_app'
        HELM_CHART_REPO = "github.com/Loli2601/weekly_calendar_app_chart.git"
        HELM_CHART_PATH = 'calendar_app/'
        COMMIT_MESSAGE = "Updated chart version by Jenkins to 1.0.${env.BUILD_NUMBER}"
    }

    stages {
        stage("Checkout code") {
            steps {
                echo "Logging ID: ${env.LOGGING_ID} - Checking out code"
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${env.BRANCH_NAME}"]],
                    userRemoteConfigs: [[
                        credentialsId: 'GitHub-cred',
                        url: 'https://github.com/Loli2601/weekly_calendar_app'
                    ]]
                ])
            }
        }

        stage("Setup Environment") {
            steps {
                echo "Logging ID: ${env.LOGGING_ID} - Setting up environment"
                sh "apk update && apk add py-pip"
                sh "pip install -r requirements.txt -r tests/requirements.txt"
            }
        }

        stage("Build Docker Image") {
            when {
                branch pattern: "feature/.*", comparator: "REGEXP"
            }
            steps {
                echo "Logging ID: ${env.LOGGING_ID} - Building Docker image"
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${env.BRANCH_NAME}-${env.BUILD_NUMBER}", "--no-cache .")
                }
            }
        }

        stage("Run tests") {
            steps {
                echo "Logging ID: ${env.LOGGING_ID} - Running tests"
                sh "pytest --cov"
            }
        }

        stage('Create merge request') {
            when {
                branch pattern: "feature/.*", comparator: "REGEXP"
            }
            steps {
                echo "Logging ID: ${env.LOGGING_ID} - Creating merge request"
                withCredentials([usernamePassword(credentialsId: 'GitHub-cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    script {
                        def branchName = env.BRANCH_NAME
                        def pullRequestTitle = "Merge ${branchName} into main"
                        def pullRequestBody = "Automatically generated merge request for branch ${branchName} from Jenkins"

                        sh """
                            curl -X POST -u ${USERNAME}:${PASSWORD} \
                            -d '{ "title": "${pullRequestTitle}", "body": "${pullRequestBody}", "head": "${branchName}", "base": "main" }' \
                            ${GITHUB_API_URL}/repos/${GITHUB_REPO}/pulls
                        """
                    }
                }
            }
        }

        stage('Merge Code') {
            when {
                branch 'main'
            }
            steps {
                echo "Logging ID: ${env.LOGGING_ID} - Merging code"
                // Assuming the merge is handled by the merge request process
            }
        }

        stage('Release Actions') {
            when {
                branch 'main'
            }
            steps {
                echo "Logging ID: ${env.LOGGING_ID} - Performing release actions"
                script {
                    // Additional release actions can be added here
                }
            }
        }

        stage('Push Docker image') {
            when {
                branch 'main'
            }
            steps {
                echo "Logging ID: ${env.LOGGING_ID} - Pushing Docker image"
                script {
                    docker.withRegistry(DOCKERHUB_URL, 'DockerHub-cred') {
                        dockerImage.push("1.0.${env.BUILD_NUMBER}")
                    }
                }
            }
        }

        stage('Clean Workspace') {
            when {
                branch 'main'
            }
            steps {
                echo "Logging ID: ${env.LOGGING_ID} - Cleaning workspace"
                cleanWs()
            }
        }

        stage('Checkout Helm Chart Repo') {
            when {
                branch 'main'
            }
            steps {
                echo "Logging ID: ${env.LOGGING_ID} - Checking out Helm chart repo"
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/main"]],
                    userRemoteConfigs: [[
                        credentialsId: 'GitHub-cred',
                        url: "https://${env.HELM_CHART_REPO}"
                    ]]
                ])
            }
        }

        stage('Update Helm Chart') {
            when {
                branch 'main'
            }
            steps {
                echo "Logging ID: ${env.LOGGING_ID} - Updating Helm chart"
                script {
                    sh """
                    sed -i 's/version:.*/version: "1.0.${env.BUILD_NUMBER}"/' ${env.HELM_CHART_PATH}values.yaml
                    sed -i 's/version:.*/version: 1.0.${env.BUILD_NUMBER}/' ${env.HELM_CHART_PATH}Chart.yaml
                    echo "Helm chart updated to version 1.0.${env.BUILD_NUMBER}"
                    """
                }
            }
        }

        stage('Commit Changes to chart repo') {
            when {
                branch 'main'
            }
            steps {
                echo "Logging ID: ${env.LOGGING_ID} - Committing changes to chart repo"
                script {
                    withCredentials([usernamePassword(credentialsId: 'GitHub-cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        sh """
                        git config --global --add safe.directory ${WORKSPACE}
                        git config user.name "jenkins"
                        git config user.email "jenkins@example.com"
                        git add .
                        git commit -m "${COMMIT_MESSAGE}"
                        git push https://${USERNAME}:${PASSWORD}@github.com/Loli2601/weekly_calendar_app_chart.git HEAD:main
                        """
                    }
                }
            }
        }

        stage('Archive Jenkinsfile') {
            when {
                branch 'main'
            }
            steps {
                echo "Logging ID: ${env.LOGGING_ID} - Archiving Jenkinsfile"
                archiveArtifacts artifacts: 'Jenkinsfile', followSymlinks: false
            }
        }
    }
}
