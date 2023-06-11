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
        echo "${USER}"
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
          kubernetesDeploy(configs: 'mysql-deploy.yml', kubeconfigId: 'kubeconfig')
          kubernetesDeploy(configs: 'mysql-service.yml', kubeconfigId: 'kubeconfig')
          kubernetesDeploy(configs: 'app-deploy.yml', kubeconfigId: 'kubeconfig')
          kubernetesDeploy(configs: 'app-service.yml', kubeconfigId: 'kubeconfig')
        }
      }
    }
  }
}
