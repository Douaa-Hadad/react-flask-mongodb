pipeline {
    agent any

    environment {
        IMAGE_NAME = "dinobear/react-flask-mongodb"
        IMAGE_TAG = "latest"
        DOCKER_CREDENTIALS = "dockerhub-creds" // Jenkins credential ID
    }

    stages {

        stage('Checkout SCM') {
            steps {
                git(
                    url: 'https://github.com/Douaa-Hadad/react-flask-mongodb.git',
                    branch: 'main',
                    credentialsId: 'github-creds'
                )
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}", "./react-flask-mongodb-v1")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS}") {
                        docker.image("${IMAGE_NAME}:${IMAGE_TAG}").push()
                    }
                }
            }
        }

        stage('Clean Up') {
            steps {
                sh "docker image prune -f"
            }
        }
    }

    post {
        success {
            echo "✅ Docker image built and pushed successfully!"
        }
        failure {
            echo "❌ Build failed. Check logs for details."
        }
    }
}
