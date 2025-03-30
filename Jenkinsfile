pipeline {
    agent any

    stages {
        stage('Clonar Repositorio') {
            steps {
                git 'https://github.com/apvasquezo/O-risk/tree/main'
            }
        }

        stage('Construir Imagen Docker') {
            steps {
                sh 'docker build -t mi-fastapi-app .'
            }
        }

        stage('Levantar Contenedor') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Pruebas') {
            steps {
                sh 'docker ps'
            }
        }
    }
}