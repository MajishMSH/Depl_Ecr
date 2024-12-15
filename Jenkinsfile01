pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'majishms/todo-list'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/MajishMSH/Depl.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${env.BUILD_NUMBER} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Use credentials ID directly instead of environment variable
                    docker.withRegistry('https://registry.hub.docker.com/', 'dockerhublogin') {
                        docker.image("${DOCKER_IMAGE}:${env.BUILD_NUMBER}").push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        sh "sed -i 's|majishms/todo-list:${env.BUILD_NUMBER}|majishms/todo-list:${env.BUILD_NUMBER}|g' k8s/deployment.yaml"
                        sh 'kubectl apply -f k8s/deployment.yaml'
                        sh 'kubectl apply -f k8s/service.yaml'
                    }
                }
            }
        }
    }
}
