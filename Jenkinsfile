pipeline {
    agent any
    environment {
        IMAGE_NAME = "dinobear/react-flask-mongodb:latest"
    }
    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME ./react-flask-mongodb-v1'
            }
        }
        stage('Run Docker Container') {
            steps {
                sh 'docker run -d -p 3000:3000 --name react-flask-mongodb $IMAGE_NAME'
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'docker login -u $USER -p $PASS'
                    sh 'docker push $IMAGE_NAME'
                }
            }
        }
    }
    post {
        always {
            sh 'docker stop react-flask-mongodb || true'
            sh 'docker rm react-flask-mongodb || true'
        }
    }
}
