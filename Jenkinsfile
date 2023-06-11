pipeline {
  environment {
    dockerimagename = "serapf/flaskapi"
    dockerImage = ""
  }
  agent any
  stages {
    stage('Checkout Source') {
      steps {
        git 'https://github.com/AlexisAguileraValderrama/Flask-Kubernetes-AF.git'
      }
    }
    stage('Build image') {
      steps{
        script {
          dockerImage = docker.build dockerimagename
        }
      }
    }
    stage('Pushing Image') {
      environment {
               registryCredential = 'Docker_hub'
           }
      steps{
        script {
          docker.withRegistry( 'https://registry.hub.docker.com', registryCredential ) {
            dockerImage.push("latest")
          }
        }
      }
    }
    stage('Deploying React.js container to Kubernetes') {
      steps {
        script {
          kubernetesDeploy(configs: "mysql-deploy.yaml", "mysql-service.yaml")
          kubernetesDeploy(configs: "app-deploy.yaml", "app-service.yaml")
        }
      }
    }
  }
}
