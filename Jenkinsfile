pipeline {
    agent any

    stages {
         stage ('Down containers'){
      steps{
        script {
            if (isUnix()) {
               sh 'docker compose down'
            } else {
                bat 'docker compose down'
            }
        }
      }
    }
    stage('Build and up containers'){
      steps{
        script{
          if (isUnix()) {
            sh 'docker compose up --build -d'
          } else {
            bat 'docker compose up --build -d'
          }
        }
      }
    }
}
}