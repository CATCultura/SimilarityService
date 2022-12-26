pipeline {
    agent any

    stages {
        stage('SonarQube Analysis') {
            steps {
                sh 'sonar-scanner -Dsonar.projectKey=SimilarityService -Dsonar.sources=. -Dsonar.host.url=http://10.4.41.41:9000 -Dsonar.login=sqp_87a5da6fede32be5cab8636bdf42cbe64b13e0c9'
            }
        }

        stage('Deploy') {
            steps {
                sh 'sudo docker kill $(sudo docker ps -q -f ancestor=similarity-service)'
                sh 'sudo docker rmi similarity-service -f'
                sh 'sudo docker build -t similarity-service .'
                sh 'sudo docker run -d -p 5500:5500 -v simservice-models:/py-service/data similarity-service'
                }
            }

       stage('Notify') {
           steps {
              discordSend description: "Similarity service successful build", footer: "Results from a build", link: env.BUILD_URL, result: currentBuild.currentResult, title: JOB_NAME, webhookURL: "https://discord.com/api/webhooks/1029023402079572108/PSi21wQLj8EdmwAYw6DbyEsGuppRKibwV7r81QVq743lG5Z3_qZw2vNIr5jJ_sU_15RZ"
           }
        }

    }
}