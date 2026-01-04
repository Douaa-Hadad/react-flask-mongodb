pipeline {
    agent any

    environment {
        DOCKERHUB_CREDS = "dockerhub-creds"
        BACKEND_IMAGE = "dinobear/todo-backend"
        FRONTEND_IMAGE = "dinobear/todo-frontend"
        TAG = "latest"
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

        stage('Build Backend Image') {
            steps {
                sh "docker build -t ${BACKEND_IMAGE}:${TAG} ./backend"
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh "docker build -t ${FRONTEND_IMAGE}:${TAG} ./frontend"
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDS) {
                        sh "docker push ${BACKEND_IMAGE}:${TAG}"
                        sh "docker push ${FRONTEND_IMAGE}:${TAG}"
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
            echo "✅ CI/CD Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs."
        }
    }
}
