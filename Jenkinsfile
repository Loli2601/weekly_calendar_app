pipeline {
    agent {
        kubernetes {
            yamlFile 'runner.yaml'
            defaultContainer 'builder'
        }
    }

    environment {
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
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/main"]],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
                    userRemoteConfigs: [[
                        credentialsId: 'GitHub-cred',
                        url: 'https://github.com/Loli2601/weekly_calendar_app'
                    ]]
                ])
            }
        }

        stage("Setup Environment") {
            steps {
                sh "apk update && apk add py-pip"
                sh "pip install -r requirements.txt -r tests/requirements.txt"
            }
        }

        stage("Run tests") {
            steps {
                sh "pytest --cov"
            }
        }

        stage("Build Docker Image") {
            when {
                branch pattern: "feature/.*", comparator: "REGEXP"
            }
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${env.BRANCH_NAME}-${env.BUILD_NUMBER}", "--no-cache .")
                }
            }
        }

        stage('Create merge request') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
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

        stage('Push Docker image') {
            when {
                branch 'main'
            }
            steps {
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
                cleanWs()
            }
        }

        stage('Checkout Helm Chart Repo') {
            when {
                branch 'main'
            }
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/main"]],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
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
                archiveArtifacts artifacts: 'Jenkinsfile', followSymlinks: false
            }
        }
    }
}

